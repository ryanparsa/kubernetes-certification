#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Create the course/ directory and copy kustomize structure into it
mkdir -p "$SCRIPT_DIR/../course"
cp -r "$SCRIPT_DIR/api-gateway" "$SCRIPT_DIR/../course/api-gateway"

# Create the namespaces required by staging and prod overlays
kubectl create namespace api-gateway-staging --kubeconfig "$KUBECONFIG_FILE"
kubectl create namespace api-gateway-prod --kubeconfig "$KUBECONFIG_FILE"

# Deploy staging and prod using kustomize
kubectl kustomize "$SCRIPT_DIR/../course/api-gateway/staging" \
  | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

kubectl kustomize "$SCRIPT_DIR/../course/api-gateway/prod" \
  | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

echo "Waiting for deployments to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n api-gateway-staging \
  deployment/api-gateway --timeout=120s
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n api-gateway-prod \
  deployment/api-gateway --timeout=120s

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
