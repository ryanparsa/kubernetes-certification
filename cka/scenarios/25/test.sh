#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check NetworkPolicy existence
NP=$(kubectl -n restricted get networkpolicy restrict-egress -o json 2>/dev/null)
if [[ $? -ne 0 ]]; then
  fail "NetworkPolicy 'restrict-egress' not found in namespace 'restricted'."
fi

# Check PodSelector
SELECTOR=$(echo "$NP" | jq -r '.spec.podSelector.matchLabels.tier')
if [[ "$SELECTOR" != "frontend" ]]; then
  fail "Incorrect podSelector: expected 'tier=frontend', got '$SELECTOR'."
fi

# Check Egress rules
# 1. DNS (UDP 53)
DNS=$(echo "$NP" | jq -r '.spec.egress[] | select(.ports[0].port == 53 and .ports[0].protocol == "UDP")')
if [[ -z "$DNS" ]]; then
  fail "Missing egress rule for DNS (UDP 53)."
fi

# 2. External World (TCP 5432)
DB=$(echo "$NP" | jq -r '.spec.egress[] | select(.ports[0].port == 5432 and .ports[0].protocol == "TCP" and .to[0].namespaceSelector != null)')
if [[ -z "$DB" ]]; then
  fail "Missing egress rule for namespace 'external-world' on port 5432."
fi

echo "PASS"
