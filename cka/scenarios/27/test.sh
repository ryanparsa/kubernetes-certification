#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check Quota
QUOTA=$(kubectl -n quota-test get quota pod-quota -o jsonpath='{.spec.hard.pods}')
if [[ "$QUOTA" -lt 10 ]]; then
  fail "ResourceQuota 'pod-quota' still has too low a pod limit ($QUOTA)."
fi

# Check Replicas
READY=$(kubectl -n quota-test get deployment limited-app -o jsonpath='{.status.readyReplicas}')
if [[ "$READY" -ne 5 ]]; then
  fail "Deployment 'limited-app' only has $READY ready replicas, expected 5."
fi

echo "PASS"
