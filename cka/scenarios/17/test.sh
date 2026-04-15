#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl -n observability get ds node-exporter >/dev/null 2>&1 || fail "DaemonSet observability/node-exporter not found"

ready=$(kubectl -n observability get ds node-exporter -o jsonpath='{.status.numberReady}')
desired=$(kubectl -n observability get ds node-exporter -o jsonpath='{.status.desiredNumberScheduled}')
[ "$desired" = "1" ] || fail "expected 1 desired, got $desired (constraint not narrow enough)"
[ "$ready" = "1" ] || fail "expected 1 ready, got $ready"

node=$(kubectl -n observability get pods -l app=node-exporter -o jsonpath='{.items[0].spec.nodeName}' 2>/dev/null)
[ -z "$node" ] && node=$(kubectl -n observability get pods -o jsonpath='{.items[0].spec.nodeName}')
[ "$node" = "cka-task-17-worker2" ] || fail "pod must run on cka-task-17-worker2 (got $node)"

echo "PASS"
