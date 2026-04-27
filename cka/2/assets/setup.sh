#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
CLUSTER_NAME="cka-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker helm; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
mkdir -p "$SCRIPT_DIR/../lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Add the MinIO Helm repository
helm repo add minio https://operator.min.io
helm repo update

# 4. Create the lab/ output directory and seed the tenant YAML
cp "$SCRIPT_DIR/minio-tenant.yaml" "$SCRIPT_DIR/../lab/minio-tenant.yaml"

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
