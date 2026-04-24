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
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  echo "Cluster $CLUSTER_NAME already exists."
  if [[ ! -f "$KUBECONFIG_FILE" ]]; then
    kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
  fi
fi

# 3. Apply pre-existing workloads
# N/A

# 4. Wait for deployments
# N/A

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 6. Copy task assets
# N/A

# 7. Print summary
echo ""
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
echo "To access the control-plane node: docker exec -it $CLUSTER_NAME-control-plane bash"
