#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create cluster
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
    kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
    kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# 2. Create the output directory
mkdir -p "$SCRIPT_DIR/../lab"

echo "Lab ready!"
echo "To start the lab, run:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
