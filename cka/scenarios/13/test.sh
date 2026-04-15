#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl get nodes >/dev/null 2>&1 || fail "API server not reachable after restore"

kubectl get namespace keepme >/dev/null 2>&1 || fail "namespace keepme should still exist"
kubectl -n keepme get configmap important >/dev/null 2>&1 || fail "configmap keepme/important should still exist"

if kubectl get namespace junk >/dev/null 2>&1; then
  fail "namespace junk still exists — restore did not roll back post-snapshot state"
fi

echo "PASS"
