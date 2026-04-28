#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# 1. Setup local mount point
mkdir -p "$SCRIPT_DIR/course"

# 2. Determine Kubeconfig location
# In CI, we use the default kubeconfig. Locally, we use a dedicated file.
if [[ -n "${GITHUB_ACTIONS:-}" ]]; then
    KUBECONFIG_FILE="${HOME}/.kube/config"
else
    KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
fi

# 3. Create cluster (if not already existing)
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

# 4. Create lab output directory
mkdir -p "$SCRIPT_DIR/../lab"

echo "Lab ready!"
if [[ -z "${GITHUB_ACTIONS:-}" ]]; then
    echo "Run: export KUBECONFIG=$KUBECONFIG_FILE"
fi
