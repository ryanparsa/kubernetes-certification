#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-6
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace shop

# Deployment with label app=web, but Service selects app=webapp (mismatch)
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: shop
spec:
  replicas: 2
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
      - name: nginx
        image: nginx:1.27-alpine
        ports: [{ containerPort: 80 }]
---
apiVersion: v1
kind: Service
metadata:
  name: broken-svc
  namespace: shop
spec:
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 80
EOF

kubectl -n shop wait --for=condition=Available deployment/web --timeout=120s

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
