#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-3
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

# Seed cluster state so the etcd snapshot is meaningful
kubectl create namespace finance
kubectl -n finance create configmap ledger --from-literal=balance=42000
kubectl -n finance create deployment billing --image=nginx:1.27-alpine --replicas=2
kubectl -n finance wait --for=condition=Available deployment/billing --timeout=120s

# clean any stale snapshot inside the etcd pod from prior runs
ETCD_POD=etcd-${CLUSTER}-control-plane
kubectl -n kube-system exec "$ETCD_POD" -- rm -f /tmp/etcd-backup.db 2>/dev/null || true

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
