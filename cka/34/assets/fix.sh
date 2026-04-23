#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Apply the kustomize config changes to prod
kubectl kustomize "$SCRIPT_DIR/../course/operator/prod" | kubectl apply -f -
