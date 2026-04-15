#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check for the static pod
POD_NAME=$(kubectl get pods -A --no-headers | grep "agent-cka-task-28-worker" | awk '{print $2}')
if [[ -z "$POD_NAME" ]]; then
  fail "Static pod 'agent' not found on cka-task-28-worker."
fi

# Check resources
CPU=$(kubectl get pod "$POD_NAME" -o jsonpath='{.spec.containers[0].resources.requests.cpu}')
MEM=$(kubectl get pod "$POD_NAME" -o jsonpath='{.spec.containers[0].resources.requests.memory}')

if [[ "$CPU" != "10m" || "$MEM" != "20Mi" ]]; then
  fail "Incorrect resources for static pod: CPU $CPU, MEM $MEM."
fi

echo "PASS"
