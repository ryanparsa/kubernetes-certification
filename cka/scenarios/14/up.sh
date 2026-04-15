#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-14
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

# Install Gateway API standard CRDs (v1.2.0). Requires internet.
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Pre-create a stub GatewayClass so the user doesn't need to invent a controller name
kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: example-class
spec:
  controllerName: example.net/gateway-controller
EOF

# Backing services for the routing task
kubectl create namespace shop
kubectl -n shop create deployment stable --image=nginx:1.27-alpine
kubectl -n shop expose deployment stable --port=80
kubectl -n shop create deployment canary --image=nginx:1.27-alpine
kubectl -n shop expose deployment canary --port=80

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
