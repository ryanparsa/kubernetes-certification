#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# Create cluster with port 30080 mapped
kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Install Gateway API standard CRDs
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Install nginx-gateway-fabric CRDs and controller (NodePort mode, port 30080)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.5.0/deploy/crds.yaml
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.5.0/deploy/nodeport/deploy.yaml

# Wait for nginx-gateway-fabric controller to be ready
echo "Waiting for nginx-gateway-fabric to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" \
  -n nginx-gateway deployment/nginx-gateway --timeout=180s

# Apply namespaces and backend workloads
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/workloads.yaml"

# Wait for backend pods
kubectl wait --kubeconfig "$KUBECONFIG_FILE" \
  -n project-r500 pod/web-desktop pod/web-mobile \
  --for=condition=Ready --timeout=60s

# Apply the Gateway resource (requires CRDs to be installed first)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/gateway.yaml"

# Create the course/ directory and put the old ingress yaml there
mkdir -p "$SCRIPT_DIR/../course"
cp "$SCRIPT_DIR/task-ingress.yaml" "$SCRIPT_DIR/../course/ingress.yaml"

echo ""
echo "Lab ready!"
echo ""
echo "NOTE: To use 'curl r500.gateway:30080/...', add this to /etc/hosts:"
echo "  127.0.0.1 r500.gateway"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
