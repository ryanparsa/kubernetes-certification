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
# Create a local directory that will be mounted into the control-plane node
mkdir -p "$SCRIPT_DIR/course"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
# N/A

# 4. Wait for deployments
echo "Waiting for CoreDNS to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n kube-system deployment/coredns --timeout=120s

# 5. Create the lab/ output directory
# Already created in step 2

# 6. Copy task assets
# N/A

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=cka/95/lab/kubeconfig.yaml"
echo ""
echo "To access the control-plane node:"
echo "  docker exec -it ${CLUSTER_NAME}-control-plane bash"
