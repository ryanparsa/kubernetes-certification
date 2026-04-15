#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-24 --kubeconfig "$KUBECONFIG"

kubectl create ns internal

# Deploy target service
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: internal
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: web
        image: nginx:1.27-alpine
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: internal
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: api
EOF

echo "Service api-service created in namespace 'internal'."
