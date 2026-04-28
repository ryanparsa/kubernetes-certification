#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Create namespace
kubectl create namespace configuration --dry-run=client -o yaml | kubectl apply -f -

# Create ConfigMap
kubectl create configmap app-config -n configuration \
  --from-literal=DB_HOST=mysql \
  --from-literal=DB_PORT=3306 \
  --from-literal=DB_NAME=myapp \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Secret
kubectl create secret generic app-secret -n configuration \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASSWORD=s3cr3t \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  namespace: configuration
spec:
  containers:
  - name: nginx
    image: nginx
    envFrom:
    - configMapRef:
        name: app-config
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/app-secret
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: app-secret
EOF

# Wait for pod to be ready
kubectl wait pod/app-pod -n configuration --for=condition=Ready --timeout=60s
