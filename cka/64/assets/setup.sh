#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
CLUSTER_NAME="cka-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$TASK_DIR/lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Install Calico CNI for NetworkPolicy support
echo "Installing Calico..."
kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml

# Wait for nodes to be ready (which happens after CNI is up)
echo "Waiting for node(s) to be ready..."
kubectl --kubeconfig "$KUBECONFIG_FILE" wait --for=condition=Ready nodes --all --timeout=300s

# Create namespace
kubectl --kubeconfig "$KUBECONFIG_FILE" create namespace network

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=cka/64/assets/kubeconfig.yaml"
