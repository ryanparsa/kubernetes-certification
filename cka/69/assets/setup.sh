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
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Install Calico CNI for NetworkPolicy support
echo "Installing Calico..."
kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml

# 4. Wait for nodes to be ready (which happens after CNI is up)
echo "Waiting for node(s) to be ready..."
kubectl --kubeconfig "$KUBECONFIG_FILE" wait --for=condition=Ready nodes --all --timeout=300s

# 5. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
