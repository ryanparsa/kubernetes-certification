#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Create namespace
kubectl create namespace observability --dry-run=client -o yaml | kubectl apply -f -

# Create pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: probes-pod
  namespace: observability
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 5
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 3
EOF

# Wait for pod to be ready
kubectl wait pod/probes-pod -n observability --for=condition=Ready --timeout=60s
