#!/usr/bin/env bash
set -euo pipefail

# 1. Check dependencies
for cmd in kind kubectl; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "$cmd is not installed. Please install it to proceed."
        exit 1
    fi
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 2. Create cluster
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

# Respect existing KUBECONFIG if set (for CI), otherwise use the local one
if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# 3. Apply pre-existing workloads
# N/A

# 4. Wait for deployments
# N/A

# 5. Create the output directory
mkdir -p "$SCRIPT_DIR/../lab"

# 6. Copy task assets
# N/A

# 7. Print summary
echo "Lab ready! To start, run:"
echo "  export KUBECONFIG=$(realpath "$KUBECONFIG_FILE")"
echo "  kubectl get nodes"
