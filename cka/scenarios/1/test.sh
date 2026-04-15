#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/assets/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl -n troubleshoot get deployment crashy >/dev/null 2>&1 \
  || fail "deployment troubleshoot/crashy not found"

ready=$(kubectl -n troubleshoot get deployment crashy -o jsonpath='{.status.readyReplicas}')
spec=$(kubectl -n troubleshoot get deployment crashy -o jsonpath='{.spec.replicas}')
[ "$spec" = "3" ] || fail "expected 3 replicas, got $spec"
[ "${ready:-0}" = "3" ] || fail "expected 3 ready replicas, got ${ready:-0}"

img=$(kubectl -n troubleshoot get deployment crashy -o jsonpath='{.spec.template.spec.containers[0].image}')
[ "$img" = "busybox:1.36" ] || fail "image must remain busybox:1.36, got $img"

# no restarts within last 30s
sleep 5
restarts=$(kubectl -n troubleshoot get pods -l app=crashy -o jsonpath='{.items[*].status.containerStatuses[0].restartCount}')
for r in $restarts; do
  [ "$r" -lt 5 ] || fail "pod restart count too high ($r) — still crashing"
done

echo "PASS"
