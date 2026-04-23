#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# In the real exam this would install the updated kubelet/kubectl packages
# and run kubeadm join. In the kind lab both nodes already run the same
# version and are joined, so we just print the join command for practice.
echo "Nodes in cluster:"
kubectl get nodes -o wide

echo ""
echo "Join command (for practice):"
kubeadm token create --print-join-command
