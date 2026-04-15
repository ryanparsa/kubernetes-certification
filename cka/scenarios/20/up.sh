#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

# Create cluster with worker node
kind create cluster --name cka-task-20 --kubeconfig "$KUBECONFIG" --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
EOF

# Break kubelet on the worker by corrupting its config file
# We'll point staticPodPath to a non-existent file or similar, but a better break is changing the port to something invalid
docker exec cka-task-20-worker bash -c "sed -i 's/address: 0.0.0.0/address: 999.999.999.999/' /var/lib/kubelet/config.yaml && systemctl restart kubelet"

echo "Kubelet sabotaged on worker node."
