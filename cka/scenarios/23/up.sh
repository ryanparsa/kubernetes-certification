#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-23 --kubeconfig "$KUBECONFIG"

# Create a local directory on the control-plane node for storage
docker exec cka-task-23-control-plane mkdir -p /mnt/data
docker exec cka-task-23-control-plane bash -c "echo 'hello from node' > /mnt/data/index.html"

echo "Directory /mnt/data created on control-plane node."
