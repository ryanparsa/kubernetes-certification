#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
mkdir -p "$SCRIPT_DIR/../lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
# Create the operator-prod namespace before applying kustomize
kubectl --kubeconfig "$KUBECONFIG_FILE" create namespace operator-prod

# 4. Wait for deployments
# (Empty in this case, will wait after applying workloads)

# 5. Create the lab/ output directory
cp -r "$SCRIPT_DIR/operator" "$SCRIPT_DIR/../lab/operator"

# Apply the initial (broken RBAC) kustomize config
kubectl kustomize "$SCRIPT_DIR/../lab/operator/prod" | kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f -

# Wait for the operator deployment to be ready
kubectl --kubeconfig "$KUBECONFIG_FILE" -n operator-prod \
  rollout status deployment/operator --timeout=120s

# 6. Copy task kubeconfig
# (Kubeconfig is already in assets/kubeconfig.yaml)

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
echo ""
echo "The kustomize operator config is at: cka/34/lab/operator"
echo "Navigate there to make changes:"
echo "  cd cka/34/lab/operator"
