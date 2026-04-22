#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Create the operator-prod namespace before applying kustomize
kubectl create namespace operator-prod --kubeconfig "$KUBECONFIG_FILE"

# Copy the kustomize operator structure into the course directory
mkdir -p "$SCRIPT_DIR/../course"
cp -r "$SCRIPT_DIR/operator" "$SCRIPT_DIR/../course/operator"

# Apply the initial (broken RBAC) kustomize config
kubectl kustomize "$SCRIPT_DIR/../course/operator/prod" | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

# Wait for the operator deployment to be ready
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n operator-prod \
  deployment/operator --timeout=120s

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
echo ""
echo "The kustomize operator config is at: cka/34/course/operator"
echo "Navigate there to make changes:"
echo "  cd cka/34/course/operator"
