#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl get nodes >/dev/null 2>&1 || fail "kubectl cannot reach the API server"

ready=$(kubectl get nodes -o jsonpath='{.items[0].status.conditions[?(@.type=="Ready")].status}')
[ "$ready" = "True" ] || fail "control-plane node not Ready"

for c in kube-apiserver kube-controller-manager kube-scheduler etcd; do
  phase=$(kubectl -n kube-system get pod -l component=$c -o jsonpath='{.items[0].status.phase}' 2>/dev/null)
  [ "$phase" = "Running" ] || fail "$c not Running (phase=$phase)"
done

echo "PASS"
