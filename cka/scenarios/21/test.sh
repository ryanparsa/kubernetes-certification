#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check for 2 containers
COUNT=$(kubectl get pod app -o jsonpath='{.spec.containers[*].name}' | wc -w | tr -d ' ')
if [[ "$COUNT" -ne 2 ]]; then
  fail "Pod 'app' should have 2 containers, but has $COUNT."
fi

# Check for sidecar container
NAME=$(kubectl get pod app -o jsonpath='{.spec.containers[?(@.name=="sidecar")].name}')
if [[ "$NAME" != "sidecar" ]]; then
  fail "Container 'sidecar' not found in Pod 'app'."
fi

# Check logs
LOGS=$(kubectl logs app -c sidecar --tail=1)
if [[ -z "$LOGS" ]]; then
  fail "No logs found in sidecar container."
fi

echo "PASS"
