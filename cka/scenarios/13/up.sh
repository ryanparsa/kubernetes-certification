#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-13
NODE=${CLUSTER}-control-plane
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

# State A: create the "good" object that must exist after the restore
kubectl create namespace keepme
kubectl -n keepme create configmap important --from-literal=key=value

# Take a snapshot of state A and copy it to a hostPath visible to the etcd pod
ETCD_POD=etcd-${NODE}
kubectl -n kube-system exec "$ETCD_POD" -- sh -c '
ETCDCTL_API=3 etcdctl snapshot save /var/lib/etcd/snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
'
# /var/lib/etcd is hostPath-mounted from the node — copy snapshot to /opt/snapshot.db on the node
docker exec "$NODE" sh -c 'cp /var/lib/etcd/snapshot.db /opt/snapshot.db && ls -lh /opt/snapshot.db'

# State B: create "junk" objects AFTER the snapshot — restore must remove them
kubectl create namespace junk
kubectl -n junk create configmap garbage --from-literal=trash=yes
kubectl -n junk create deployment junkapp --image=nginx:1.27-alpine

echo
echo "Snapshot is at /opt/snapshot.db on node $NODE"
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
