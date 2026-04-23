#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads

# 4. Wait for deployments
echo "Waiting for etcd to be ready..."
kubectl wait --kubeconfig "$KUBECONFIG_FILE" -n kube-system --for=condition=Ready pod -l component=etcd --timeout=120s

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 6. Copy task assets

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "To access the control plane node (needed for etcdctl snapshot):"
echo "  docker exec -it $CLUSTER_NAME-control-plane bash"
echo ""
echo "Inside the node, output files go to /opt/course/$LAB_ID/ (mapped to $EXAM/$LAB_ID/course/ on your host)."
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
