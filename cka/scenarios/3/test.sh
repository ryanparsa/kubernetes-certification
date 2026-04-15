#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"
ETCD_POD=etcd-cka-task-3-control-plane

fail() { echo "FAIL: $*"; exit 1; }

kubectl -n kube-system get pod "$ETCD_POD" >/dev/null 2>&1 || fail "etcd pod not found"

# file exists and non-empty
size=$(kubectl -n kube-system exec "$ETCD_POD" -- sh -c 'wc -c < /tmp/etcd-backup.db 2>/dev/null || echo 0')
[ "${size:-0}" -gt 0 ] 2>/dev/null || fail "/tmp/etcd-backup.db missing or empty inside etcd pod"

# valid snapshot
kubectl -n kube-system exec "$ETCD_POD" -- sh -c '
  ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key
' >/dev/null 2>&1 || fail "etcdctl snapshot status reports invalid snapshot"

echo "PASS"
