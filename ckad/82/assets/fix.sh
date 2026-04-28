#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Create namespace
kubectl create namespace secrets-ns --dry-run=client -o yaml | kubectl apply -f -

# Create Secret
kubectl create secret generic db-secret -n secrets-ns \
  --from-literal=username=admin \
  --from-literal=password=SuperSecret123 \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Pod with Secret volume mount
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
  namespace: secrets-ns
spec:
  containers:
  - name: app
    image: alpine
    command: ["sleep", "3600"]
    volumeMounts:
    - name: secret-vol
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-vol
    secret:
      secretName: db-secret
EOF

# Wait for pod to be ready
kubectl wait pod/secret-pod -n secrets-ns --for=condition=Ready --timeout=60s
