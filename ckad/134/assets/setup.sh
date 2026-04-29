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

# Only create cluster if KUBECONFIG is not already set
if [[ -z "${KUBECONFIG:-}" ]]; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Create ConfigMap
kubectl create configmap web-server-conf --from-literal=custom.conf="server { listen 80; server_name localhost; location / { root /usr/share/nginx/html; index index.html; } }"

# Create Deployment without the volume mount
kubectl create deployment web-server --image=nginx:1.25 --replicas=1

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
