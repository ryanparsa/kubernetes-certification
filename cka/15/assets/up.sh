#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Install Calico CNI for NetworkPolicy support
echo "Installing Calico..."
kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml

# Wait for nodes to be ready (which happens after CNI is up)
echo "Waiting for node(s) to be ready..."
kubectl --kubeconfig "$KUBECONFIG_FILE" wait --for=condition=Ready nodes --all --timeout=300s

kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/workloads.yaml"

# Wait for all pods in project-snake to be ready
echo "Waiting for pods in project-snake..."
kubectl wait --kubeconfig "$KUBECONFIG_FILE" \
  -n project-snake pod/backend-0 pod/db1-0 pod/db2-0 pod/vault-0 \
  --for=condition=Ready --timeout=120s

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
