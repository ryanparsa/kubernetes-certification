#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

helm -n platform list 2>/dev/null | awk '{print $1, $NF}' | grep -q '^frontend deployed' \
  || fail "helm release 'frontend' not deployed in namespace platform"

ready=$(kubectl -n platform get deployment frontend -o jsonpath='{.status.readyReplicas}' 2>/dev/null)
[ "${ready:-0}" = "3" ] || fail "frontend deployment must have 3 ready replicas (got $ready)"

svct=$(kubectl -n platform get svc frontend -o jsonpath='{.spec.type}' 2>/dev/null)
[ "$svct" = "NodePort" ] || fail "frontend service must be type NodePort (got $svct)"

echo "PASS"
