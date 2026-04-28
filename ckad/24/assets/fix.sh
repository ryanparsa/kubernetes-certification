#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Ensure namespace exists
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -

# Create the ConfigMap
kubectl create configmap app-config -n workloads \
  --from-literal=APP_ENV=production \
  --from-literal=LOG_LEVEL=info \
  --dry-run=client -o yaml | kubectl apply -f -

# Create the Pod with ConfigMap environment variables and resource limits
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
  namespace: workloads
spec:
  containers:
  - name: nginx
    image: nginx
    env:
    - name: APP_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
EOF

kubectl wait pod config-pod -n workloads --for=condition=Ready --timeout=60s
