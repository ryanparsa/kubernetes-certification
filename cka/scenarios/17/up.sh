#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-17
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG" --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF

kubectl wait --for=condition=Ready node --all --timeout=240s

# Label only worker2 — worker (and control-plane) get nothing
kubectl label node ${CLUSTER}-worker2 monitoring=true --overwrite

kubectl create namespace observability

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
