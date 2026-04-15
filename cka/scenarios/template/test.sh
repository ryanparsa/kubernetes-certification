#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/assets/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

# TODO: add assertions here
# Examples:
#   kubectl get pod my-pod >/dev/null 2>&1 || fail "pod my-pod not found"
#   phase=$(kubectl get pod my-pod -o jsonpath='{.status.phase}')
#   [ "$phase" = "Running" ] || fail "expected Running, got $phase"

echo "PASS"
