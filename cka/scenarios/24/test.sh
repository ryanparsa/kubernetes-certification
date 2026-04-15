#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check Ingress
INGRESS=$(kubectl -n internal get ingress api-ingress -o json 2>/dev/null)
if [[ $? -ne 0 ]]; then
  fail "Ingress 'api-ingress' not found in namespace 'internal'."
fi

HOST=$(echo "$INGRESS" | jq -r '.spec.rules[0].host')
if [[ "$HOST" != "api.example.com" ]]; then
  fail "Incorrect host: expected 'api.example.com', got '$HOST'."
fi

PATH_VAL=$(echo "$INGRESS" | jq -r '.spec.rules[0].http.paths[0].path')
if [[ "$PATH_VAL" != "/v1" ]]; then
  fail "Incorrect path: expected '/v1', got '$PATH_VAL'."
fi

SVC=$(echo "$INGRESS" | jq -r '.spec.rules[0].http.paths[0].backend.service.name')
if [[ "$SVC" != "api-service" ]]; then
  fail "Incorrect backend service: expected 'api-service', got '$SVC'."
fi

echo "PASS"
