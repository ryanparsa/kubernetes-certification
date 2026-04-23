#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# Delete the cluster
kind delete cluster --name "$CLUSTER_NAME"

# Remove generated directories
rm -rf "$SCRIPT_DIR/../course"
rm -f "$SCRIPT_DIR/kubeconfig.yaml"

echo "Lab torn down."
