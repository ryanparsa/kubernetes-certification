#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-5
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace web
kubectl -n web run api --image=nginx:1.27-alpine --labels=app=api --port=8080
kubectl -n web run frontend --image=nginx:1.27-alpine --labels=role=frontend
kubectl -n web run other    --image=nginx:1.27-alpine --labels=role=other

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
