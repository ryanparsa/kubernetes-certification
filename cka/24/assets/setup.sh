#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# Create the lab/ output directory before starting kind
# (kind-config.yaml mounts it as /opt/course/7 in the container)
mkdir -p "$SCRIPT_DIR/../lab"

# Change to assets dir so the relative hostPath in kind-config.yaml resolves correctly
cd "$SCRIPT_DIR"
kind create cluster --name "$CLUSTER_NAME" --config kind-config.yaml --kubeconfig "$KUBECONFIG_FILE"

# Wait for etcd to be ready
echo "Waiting for etcd to be ready..."
kubectl --kubeconfig "$KUBECONFIG_FILE" wait -n kube-system --for=condition=Ready pod -l component=etcd --timeout=120s

echo ""
echo "Lab ready!"
echo ""
echo "To access the control plane node (needed for etcdctl snapshot):"
echo "  docker exec -it ${CLUSTER_NAME}-control-plane bash"
echo ""
echo "Inside the node, output files go to /opt/course/7/ (mapped to cka/24/lab/ on your host)."
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
