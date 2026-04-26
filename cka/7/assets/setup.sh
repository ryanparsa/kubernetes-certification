#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
CLUSTER_NAME="cka-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Install metrics-server with kubelet-insecure-tls (required for kind)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch deployment metrics-server \
  --kubeconfig "$KUBECONFIG_FILE" \
  -n kube-system \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

echo "Waiting for metrics-server to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" \
  -n kube-system deployment/metrics-server --timeout=120s

# Create the course/ output directory for the user's scripts
mkdir -p "$SCRIPT_DIR/../course"

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
