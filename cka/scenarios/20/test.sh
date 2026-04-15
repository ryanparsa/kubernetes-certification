#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check node status
STATUS=$(kubectl get node cka-task-20-worker -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)
if [[ "$STATUS" != "True" ]]; then
  fail "Node cka-task-20-worker is not Ready."
fi

echo "PASS"
