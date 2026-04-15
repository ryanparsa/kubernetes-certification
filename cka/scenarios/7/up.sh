#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-7
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG" --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
EOF

kubectl wait --for=condition=Ready node --all --timeout=240s

WORKER=${CLUSTER}-worker
kubectl label node "$WORKER" disk=ssd --overwrite
kubectl taint node "$WORKER" tier=critical:NoSchedule --overwrite

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
