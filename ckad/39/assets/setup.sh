#!/usr/bin/env bash
set -euo pipefail

# 1. Check dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 2. Create cluster
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
# N/A

# 4. Wait for deployments
# N/A

# 5. Create the output directory
mkdir -p "$SCRIPT_DIR/../lab"

# 6. Copy task assets
# N/A

# 7. Print summary
echo "Lab ready!"
echo "Run: export KUBECONFIG=$KUBECONFIG_FILE"
echo "You can now work on the lab in the ckad/39 directory."
