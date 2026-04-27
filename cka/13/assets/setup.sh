#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster (only if it doesn't exist and we're not in CI)
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

# 3. Apply pre-existing workloads
# Install Gateway API standard CRDs
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Install nginx-gateway-fabric CRDs and controller (NodePort mode, port 30080)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.5.0/deploy/crds.yaml
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.5.0/deploy/nodeport/deploy.yaml

# Apply namespaces and backend workloads
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/workloads.yaml"

# Apply the Gateway resource (requires CRDs to be installed first)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/gateway.yaml"

# 4. Wait for deployments
echo "Waiting for nginx-gateway-fabric to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" \
  -n nginx-gateway deployment/nginx-gateway --timeout=180s

echo "Waiting for backend pods..."
kubectl wait --kubeconfig "$KUBECONFIG_FILE" \
  -n project-r500 pod/web-desktop pod/web-mobile \
  --for=condition=Ready --timeout=60s

# 5. Create the lab/ output directory
mkdir -p "$TASK_DIR/lab"

# 6. Copy task assets
cp "$SCRIPT_DIR/task-ingress.yaml" "$TASK_DIR/lab/ingress.yaml"

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "NOTE: To use 'curl r500.gateway:30080/...', add this to /etc/hosts:"
echo "  127.0.0.1 r500.gateway"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
