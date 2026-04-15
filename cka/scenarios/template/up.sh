#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-N
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/assets/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl apply -f "$DIR/assets/manifest.yaml"

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
