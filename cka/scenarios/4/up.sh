#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-4
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace dev
kubectl create namespace prod

# seed a few pods so list/get returns something
kubectl -n dev run sample --image=nginx:1.27-alpine

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
