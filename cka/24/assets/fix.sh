#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# 1. Extract etcd version
ETCD_POD=$(kubectl -n kube-system get pod -l component=etcd -o name | head -n 1)
kubectl -n kube-system exec "$ETCD_POD" -- etcd --version > "$SCRIPT_DIR/../course/etcd-version"

# 2. Perform etcd snapshot
# We need to get authentication info from the etcd pod
ETCD_CA="/etc/kubernetes/pki/etcd/ca.crt"
ETCD_CERT="/etc/kubernetes/pki/etcd/server.crt"
ETCD_KEY="/etc/kubernetes/pki/etcd/server.key"

docker exec "$CLUSTER_NAME-control-plane" sh -c "ETCDCTL_API=3 etcdctl snapshot save /opt/course/$LAB_ID/etcd-snapshot.db \
--cacert $ETCD_CA \
--cert $ETCD_CERT \
--key $ETCD_KEY"
