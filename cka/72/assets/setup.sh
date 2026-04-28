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

# 2. Create cluster
mkdir -p "$TASK_DIR/lab"
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

# Set KUBECONFIG for the rest of the script if not in CI (where kind-action sets it)
if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# 3. Apply pre-existing workloads
# Install Gateway API standard CRDs
kubectl apply \
  -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Install nginx-gateway-fabric CRDs and controller
kubectl apply \
  -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.5.0/deploy/crds.yaml
kubectl apply \
  -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.5.0/deploy/nodeport/deploy.yaml

# Patch nginx-gateway-fabric to use NodePort 30000
kubectl patch service nginx-gateway -n nginx-gateway --type='json' -p='[{"op": "replace", "path": "/spec/ports/0/nodePort", "value": 30000}]'

# Apply namespaces and backend workloads
kubectl apply -f "$SCRIPT_DIR/workloads.yaml"

# Apply the Gateway resource
kubectl apply -f "$SCRIPT_DIR/gateway.yaml"

# 4. Wait for deployments
echo "Waiting for nginx-gateway-fabric to be ready..."
kubectl rollout status \
  -n nginx-gateway deployment/nginx-gateway --timeout=180s

echo "Waiting for backend pods..."
kubectl wait \
  -n project-r500 pod/web-desktop pod/web-mobile \
  --for=condition=Ready --timeout=60s

# 5. Create the lab/ output directory

# 6. Copy task assets
cp "$SCRIPT_DIR/task-ingress.yaml" "$TASK_DIR/lab/72-ingress.yaml"

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
