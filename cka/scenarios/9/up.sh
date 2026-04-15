#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-9
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

# Stop the kubelet on the worker — node will go NotReady within ~40s
docker exec ${CLUSTER}-worker systemctl stop kubelet

# Seed a Deployment so the user sees the impact of the broken node
kubectl create deployment hello --image=nginx:1.27-alpine --replicas=4

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
