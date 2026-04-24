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
kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f "$SCRIPT_DIR/workloads.yaml"

# 4. Wait for deployments
# N/A

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 6. Copy task assets
cp "$SCRIPT_DIR/$LAB_ID.yaml" "$SCRIPT_DIR/../course/$LAB_ID.yaml"

# 7. Print summary
echo ""
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
