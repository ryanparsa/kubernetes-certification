#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/workloads.yaml"

# Create the course/ directory and place the starting backup.yaml there
mkdir -p "$SCRIPT_DIR/../course"
cp "$SCRIPT_DIR/backup.yaml" "$SCRIPT_DIR/../course/backup.yaml"

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
