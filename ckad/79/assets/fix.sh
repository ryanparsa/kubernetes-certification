#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Create namespace (idempotent)
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -

# Apply the Pod manifest (idempotent)
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web
  namespace: workloads
  labels:
    app: web
    tier: frontend
spec:
  containers:
  - name: web
    image: nginx:1.25
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 250m
        memory: 256Mi
EOF

kubectl wait pod/web -n workloads --for=condition=Ready --timeout=120s
