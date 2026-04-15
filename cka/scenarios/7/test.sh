#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl get deployment priority-app >/dev/null 2>&1 || fail "Deployment priority-app not found"

ready=$(kubectl get deployment priority-app -o jsonpath='{.status.readyReplicas}')
[ "${ready:-0}" = "3" ] || fail "expected 3 ready replicas, got ${ready:-0}"

# all pods on the worker
nodes=$(kubectl get pods -l app=priority-app -o jsonpath='{.items[*].spec.nodeName}')
for n in $nodes; do
  [ "$n" = "cka-task-7-worker" ] || fail "pod scheduled on $n, expected cka-task-7-worker"
done

# resources set
req=$(kubectl get deployment priority-app -o jsonpath='{.spec.template.spec.containers[0].resources.requests.cpu}')
lim=$(kubectl get deployment priority-app -o jsonpath='{.spec.template.spec.containers[0].resources.limits.cpu}')
[ "$req" = "100m" ] || fail "cpu request must be 100m (got $req)"
[ "$lim" = "200m" ] || fail "cpu limit must be 200m (got $lim)"

# toleration present
tol=$(kubectl get deployment priority-app -o jsonpath='{.spec.template.spec.tolerations[*].key}')
echo "$tol" | grep -qw tier || fail "missing toleration for taint key 'tier'"

# nodeAffinity present
aff=$(kubectl get deployment priority-app -o jsonpath='{.spec.template.spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[0].matchExpressions[0].key}')
[ "$aff" = "disk" ] || fail "missing required nodeAffinity on label 'disk' (got: $aff)"

echo "PASS"
