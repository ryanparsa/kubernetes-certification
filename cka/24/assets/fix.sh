#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

COURSE_DIR="$SCRIPT_DIR/../course"
mkdir -p "$COURSE_DIR"

# Step 1: Save etcd version output
kubectl -n kube-system exec "etcd-${CLUSTER_NAME}-control-plane" -- etcd --version \
  > "$COURSE_DIR/etcd-version"

# Step 2: Create etcd snapshot (run inside the kind node where etcdctl and certs are available)
docker exec "${CLUSTER_NAME}-control-plane" bash -c "
  rm -f /opt/course/7/etcd-snapshot.db /opt/course/7/etcd-snapshot.db.part
  ETCDCTL_API=3 etcdctl snapshot save /opt/course/7/etcd-snapshot.db \
    --cacert /etc/kubernetes/pki/etcd/ca.crt \
    --cert /etc/kubernetes/pki/etcd/server.crt \
    --key /etc/kubernetes/pki/etcd/server.key
"

echo "etcd-version and etcd-snapshot.db written to course/"
