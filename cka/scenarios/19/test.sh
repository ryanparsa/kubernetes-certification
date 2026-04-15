#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check node status
STATUS=$(kubectl get node cka-task-19-worker -o jsonpath='{.spec.unschedulable}' 2>/dev/null)
if [[ "$STATUS" != "true" ]]; then
  fail "Node cka-task-19-worker is not cordoned (unschedulable=true)."
fi

# Check for pods from legacy-app on that node
PODS=$(kubectl get pods -l app=legacy --field-selector spec.nodeName=cka-task-19-worker --no-headers 2>/dev/null)
if [[ -n "$PODS" ]]; then
  fail "There are still legacy-app pods running on cka-task-19-worker."
fi

echo "PASS"
