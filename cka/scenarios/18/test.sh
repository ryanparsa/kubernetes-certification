#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

# resources patched
req=$(kubectl -n web get deployment shop -o jsonpath='{.spec.template.spec.containers[0].resources.requests.cpu}')
lim=$(kubectl -n web get deployment shop -o jsonpath='{.spec.template.spec.containers[0].resources.limits.cpu}')
[ "$req" = "200m" ] || fail "cpu request must be 200m (got $req)"
[ "$lim" = "500m" ] || fail "cpu limit must be 500m (got $lim)"

# HPA exists
kubectl -n web get hpa shop-hpa >/dev/null 2>&1 || fail "HPA web/shop-hpa not found"

api=$(kubectl -n web get hpa shop-hpa -o jsonpath='{.apiVersion}')
echo "$api" | grep -q 'autoscaling/v2' || fail "HPA must use autoscaling/v2 (got $api)"

mn=$(kubectl -n web get hpa shop-hpa -o jsonpath='{.spec.minReplicas}')
mx=$(kubectl -n web get hpa shop-hpa -o jsonpath='{.spec.maxReplicas}')
[ "$mn" = "2" ] || fail "minReplicas must be 2 (got $mn)"
[ "$mx" = "6" ] || fail "maxReplicas must be 6 (got $mx)"

target=$(kubectl -n web get hpa shop-hpa -o jsonpath='{.spec.metrics[0].resource.target.averageUtilization}')
[ "$target" = "60" ] || fail "CPU averageUtilization target must be 60 (got $target)"

ref=$(kubectl -n web get hpa shop-hpa -o jsonpath='{.spec.scaleTargetRef.name}')
[ "$ref" = "shop" ] || fail "scaleTargetRef must be Deployment shop (got $ref)"

# HPA-driven scaleup: deployment should reach >=2 replicas
for i in $(seq 1 30); do
  ready=$(kubectl -n web get deployment shop -o jsonpath='{.status.readyReplicas}' 2>/dev/null)
  [ "${ready:-0}" -ge 2 ] 2>/dev/null && break
  sleep 2
done
ready=$(kubectl -n web get deployment shop -o jsonpath='{.status.readyReplicas}')
[ "${ready:-0}" -ge 2 ] 2>/dev/null || fail "deployment did not scale to >=2 ready replicas (got $ready)"

echo "PASS"
