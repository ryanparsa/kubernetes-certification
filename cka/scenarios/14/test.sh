#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }
G() { kubectl -n shop get gateway shop-gw -o jsonpath="$1" 2>/dev/null; }
R() { kubectl -n shop get httproute shop-route -o jsonpath="$1" 2>/dev/null; }

kubectl -n shop get gateway shop-gw >/dev/null 2>&1 || fail "Gateway shop/shop-gw not found"
kubectl -n shop get httproute shop-route >/dev/null 2>&1 || fail "HTTPRoute shop/shop-route not found"

[ "$(G '{.spec.gatewayClassName}')" = "example-class" ] || fail "Gateway must use example-class"
[ "$(G '{.spec.listeners[0].port}')" = "80" ] || fail "Gateway listener port must be 80"
[ "$(G '{.spec.listeners[0].protocol}')" = "HTTP" ] || fail "Gateway listener protocol must be HTTP"
[ "$(G '{.spec.listeners[0].hostname}')" = "shop.example.com" ] || fail "Gateway listener hostname must be shop.example.com"

[ "$(R '{.spec.parentRefs[0].name}')" = "shop-gw" ] || fail "HTTPRoute parentRef must be shop-gw"

# match prefix /
mt=$(R '{.spec.rules[0].matches[0].path.type}')
mv=$(R '{.spec.rules[0].matches[0].path.value}')
[ "$mt" = "PathPrefix" ] && [ "$mv" = "/" ] || fail "HTTPRoute path match must be PathPrefix /"

# backendRefs with weights
names=$(R '{.spec.rules[0].backendRefs[*].name}')
weights=$(R '{.spec.rules[0].backendRefs[*].weight}')
echo "$names" | grep -qw stable || fail "missing backend stable"
echo "$names" | grep -qw canary || fail "missing backend canary"

# Verify per-name weight
sw=$(kubectl -n shop get httproute shop-route -o jsonpath='{range .spec.rules[0].backendRefs[*]}{.name}={.weight} {end}')
echo "$sw" | grep -q 'stable=90' || fail "stable weight must be 90 (got: $sw)"
echo "$sw" | grep -q 'canary=10' || fail "canary weight must be 10 (got: $sw)"

echo "PASS"
