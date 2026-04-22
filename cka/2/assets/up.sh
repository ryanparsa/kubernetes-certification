#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker helm; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads (none)
# Note: The task assumes the Helm repository is added, so we do it here.
helm repo add minio https://operator.min.io
helm repo update

# 5. Create the course/ output directory and seed the tenant YAML
mkdir -p "$SCRIPT_DIR/../course"
cp "$SCRIPT_DIR/minio-tenant.yaml" "$SCRIPT_DIR/../course/minio-tenant.yaml"

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
