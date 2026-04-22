#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --name cka-lab --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
# Create the operator-prod namespace before applying kustomize
kubectl --kubeconfig "$KUBECONFIG_FILE" create namespace operator-prod

# Copy the kustomize operator structure into the course directory
mkdir -p "$SCRIPT_DIR/../course"
cp -r "$SCRIPT_DIR/operator" "$SCRIPT_DIR/../course/operator"

# Apply the initial (broken RBAC) kustomize config
kubectl kustomize "$SCRIPT_DIR/../course/operator/prod" | kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f -

# Wait for the operator deployment to be ready
kubectl --kubeconfig "$KUBECONFIG_FILE" -n operator-prod \
  rollout status deployment/operator --timeout=120s

# 4. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
echo ""
echo "The kustomize operator config is at: cka/34/course/operator"
echo "Navigate there to make changes:"
echo "  cd cka/34/course/operator"
