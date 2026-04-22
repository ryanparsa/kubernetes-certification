#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
COURSE_DIR="$SCRIPT_DIR/../course"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create the course/ output directory
mkdir -p "$COURSE_DIR"

# 3. Create cluster
# Move to script directory so relative paths in kind-config.yaml resolve correctly
cd "$SCRIPT_DIR"
kind create cluster --config "kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 4. Wait for etcd to be ready
echo "Waiting for etcd to be ready..."
kubectl wait --kubeconfig "$KUBECONFIG_FILE" -n kube-system --for=condition=Ready pod -l component=etcd --timeout=120s

# 5. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "To access the control plane node (needed for etcdctl snapshot):"
echo "  docker exec -it cka-lab-control-plane bash"
echo ""
echo "Inside the node, output files go to /opt/course/7/ (mapped to cka/24/course/ on your host)."
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
