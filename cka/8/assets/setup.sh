#!/usr/bin/env bash
set -euo pipefail

# 1. Check dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Note: In the real exam, the worker node starts outside the cluster with an older"
echo "Kubernetes version. In this kind lab both nodes run the same version and the worker"
echo "is already joined — you can practise generating a join token and exploring kubeadm."
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
