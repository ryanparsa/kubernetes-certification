#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-16
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace shop

# Revision 1: a working image
kubectl -n shop create deployment store --image=nginx:1.27-alpine --replicas=3
kubectl -n shop rollout status deployment/store --timeout=120s

# Revision 2: change to a broken image (typo) — generates a new revision
kubectl -n shop set image deployment/store nginx=nginx:doesnotexist-9.9
# Don't wait — it will never be ready, that's the broken state we hand over

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
