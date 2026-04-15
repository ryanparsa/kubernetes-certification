#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

for n in cka-task-9-control-plane cka-task-9-worker; do
  s=$(kubectl get node "$n" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)
  [ "$s" = "True" ] || fail "node $n not Ready (status=$s)"
done

ready=$(kubectl get deployment hello -o jsonpath='{.status.readyReplicas}')
[ "${ready:-0}" = "4" ] || fail "deployment hello not fully ready ($ready/4)"

echo "PASS"
