#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$TASK_DIR")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$TASK_DIR/lab"

# Only create cluster if it doesn't exist
if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
  kind export kubeconfig --name "$CLUSTER_NAME" --kubeconfig "$KUBECONFIG_FILE"
else
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

# Ensure KUBECONFIG is set
export KUBECONFIG="${KUBECONFIG:-$KUBECONFIG_FILE}"

# Create ConfigMap (idempotent)
kubectl create configmap web-server-conf --from-literal=custom.conf="server { listen 80; server_name localhost; location / { root /usr/share/nginx/html; index index.html; } }" --dry-run=client -o yaml | kubectl apply -f -

# Create Deployment without the volume mount (idempotent)
kubectl create deployment web-server --image=nginx:1.25 --replicas=1 --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
