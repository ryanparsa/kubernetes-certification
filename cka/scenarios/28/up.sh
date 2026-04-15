#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-28 --kubeconfig "$KUBECONFIG" --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
EOF

# Ensure static pod directory exists on the worker
docker exec cka-task-28-worker mkdir -p /etc/kubernetes/manifests

echo "Cluster created with worker node 'cka-task-28-worker' and static pod dir /etc/kubernetes/manifests."
