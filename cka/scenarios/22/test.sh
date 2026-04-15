#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check CSR status
STATUS=$(kubectl get csr john-developer -o jsonpath='{.status.conditions[?(@.type=="Approved")].type}' 2>/dev/null)
if [[ "$STATUS" != "Approved" ]]; then
  fail "CSR john-developer is not Approved."
fi

# Check if certificate is issued
CERT=$(kubectl get csr john-developer -o jsonpath='{.status.certificate}' 2>/dev/null)
if [[ -z "$CERT" ]]; then
  fail "Certificate has not been issued for john-developer."
fi

echo "PASS"
