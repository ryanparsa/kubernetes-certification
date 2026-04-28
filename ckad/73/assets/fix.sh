#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Create Secret
kubectl create secret generic db-credentials \
  --from-literal=db-password=passwd \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: backend
  namespace: default
spec:
  containers:
  - name: backend
    image: nginx
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: db-password
  restartPolicy: Always
EOF

kubectl wait pod/backend -n default --for=condition=Ready --timeout=60s
