#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl -n shop get svc broken-svc >/dev/null 2>&1 || fail "Service shop/broken-svc missing"

# Two endpoints
ips=$(kubectl -n shop get endpoints broken-svc -o jsonpath='{.subsets[0].addresses[*].ip}' 2>/dev/null)
count=$(echo $ips | wc -w | tr -d ' ')
[ "$count" = "2" ] || fail "expected 2 endpoint IPs, got $count ($ips)"

# Active curl
kubectl -n shop run curl-test --rm -i --restart=Never --image=curlimages/curl:8.10.1 \
  --command -- curl -sf -o /dev/null -w '%{http_code}' http://broken-svc.shop.svc.cluster.local \
  2>/dev/null | grep -q 200 || fail "curl to broken-svc did not return 200"

echo "PASS"
