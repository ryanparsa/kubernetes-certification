#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-15
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace app
kubectl -n app create configmap app-config \
  --from-literal=LOG_LEVEL=info \
  --from-literal=app.properties='env=prod
region=us-east-1'
kubectl -n app create secret generic app-secret \
  --from-literal=DB_PASSWORD='s3cr3t-pa55' \
  --from-literal=API_KEY='ak_live_xyz'

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
