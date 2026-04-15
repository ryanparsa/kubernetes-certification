#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

ready=$(kubectl -n kube-system get deployment coredns -o jsonpath='{.status.readyReplicas}')
[ "${ready:-0}" -ge 1 ] 2>/dev/null || fail "coredns has no ready replicas"

# nslookup from a one-shot pod
out=$(kubectl run dnstest --rm -i --restart=Never --image=busybox:1.36 \
  --command -- nslookup web.probe.svc.cluster.local 2>&1) || true
echo "$out" | grep -q "Address" || fail "nslookup did not resolve web.probe.svc.cluster.local: $out"

echo "PASS"
