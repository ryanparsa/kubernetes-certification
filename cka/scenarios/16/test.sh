#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

img=$(kubectl -n shop get deployment store -o jsonpath='{.spec.template.spec.containers[0].image}')
[ "$img" = "nginx:1.27-alpine" ] || fail "image must be back to nginx:1.27-alpine (got $img)"

ready=$(kubectl -n shop get deployment store -o jsonpath='{.status.readyReplicas}')
[ "${ready:-0}" = "3" ] || fail "expected 3 ready replicas, got $ready"

echo "PASS"
