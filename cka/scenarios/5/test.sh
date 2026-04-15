#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }
J() { kubectl -n web get netpol "$1" -o jsonpath="$2" 2>/dev/null; }

kubectl -n web get netpol default-deny >/dev/null 2>&1 || fail "NetworkPolicy default-deny not found"
kubectl -n web get netpol allow-frontend-to-api >/dev/null 2>&1 || fail "NetworkPolicy allow-frontend-to-api not found"

# default-deny: empty podSelector, Ingress in policyTypes, no ingress rules
sel=$(J default-deny '{.spec.podSelector}')
[ "$sel" = "{}" ] || [ -z "$sel" ] || fail "default-deny.podSelector must be empty (got: $sel)"
pt=$(J default-deny '{.spec.policyTypes[*]}')
echo "$pt" | grep -qw Ingress || fail "default-deny must include Ingress in policyTypes"
rules=$(J default-deny '{.spec.ingress}')
[ -z "$rules" ] || [ "$rules" = "null" ] || fail "default-deny must have no ingress rules"

# allow-frontend-to-api
match=$(J allow-frontend-to-api '{.spec.podSelector.matchLabels.app}')
[ "$match" = "api" ] || fail "allow-frontend-to-api must select app=api"

from=$(J allow-frontend-to-api '{.spec.ingress[0].from[0].podSelector.matchLabels.role}')
[ "$from" = "frontend" ] || fail "ingress.from must select role=frontend (got: $from)"

port=$(J allow-frontend-to-api '{.spec.ingress[0].ports[0].port}')
proto=$(J allow-frontend-to-api '{.spec.ingress[0].ports[0].protocol}')
[ "$port" = "8080" ] || fail "port must be 8080 (got: $port)"
[ "$proto" = "TCP" ] || fail "protocol must be TCP (got: $proto)"

echo "PASS"
