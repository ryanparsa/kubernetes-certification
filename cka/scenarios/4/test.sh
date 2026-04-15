#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl -n dev get sa dev-reader >/dev/null 2>&1 || fail "ServiceAccount dev/dev-reader not found"
kubectl -n dev get role pod-reader >/dev/null 2>&1 || fail "Role dev/pod-reader not found"
kubectl -n dev get rolebinding dev-reader-binding >/dev/null 2>&1 || fail "RoleBinding dev/dev-reader-binding not found"

SA=system:serviceaccount:dev:dev-reader

ans=$(kubectl auth can-i list pods --as=$SA -n dev 2>/dev/null)
[ "$ans" = "yes" ] || fail "dev-reader cannot list pods in dev (got: $ans)"

ans=$(kubectl auth can-i get pods --as=$SA -n dev 2>/dev/null)
[ "$ans" = "yes" ] || fail "dev-reader cannot get pods in dev"

ans=$(kubectl auth can-i watch pods --as=$SA -n dev 2>/dev/null)
[ "$ans" = "yes" ] || fail "dev-reader cannot watch pods in dev"

ans=$(kubectl auth can-i list pods --as=$SA -n prod 2>/dev/null)
[ "$ans" = "no" ] || fail "dev-reader should NOT list pods in prod (got: $ans)"

ans=$(kubectl auth can-i delete pods --as=$SA -n dev 2>/dev/null)
[ "$ans" = "no" ] || fail "dev-reader should NOT delete pods in dev (got: $ans)"

ans=$(kubectl auth can-i list deployments --as=$SA -n dev 2>/dev/null)
[ "$ans" = "no" ] || fail "dev-reader should NOT list deployments in dev"

echo "PASS"
