#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

# base must be untouched
grep -q 'replicas: 1' "$DIR/k8s/base/deployment.yaml" || fail "base/deployment.yaml was modified — patch the overlay instead"

kubectl -n ops get deployment api >/dev/null 2>&1 || fail "Deployment ops/api not found"
ready=$(kubectl -n ops get deployment api -o jsonpath='{.status.readyReplicas}')
[ "${ready:-0}" = "4" ] || fail "expected 4 ready replicas in ops/api (got $ready)"

echo "PASS"
