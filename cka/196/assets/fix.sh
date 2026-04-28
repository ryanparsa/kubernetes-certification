#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Create Pod
kubectl run tigers-reunite -n project-tiger --image=httpd:2.4-alpine --labels "pod=container,container=pod"

# Wait for Pod to be scheduled and running
kubectl wait pod tigers-reunite -n project-tiger --for=condition=Ready --timeout=60s

# Find the node
NODE=$(kubectl get pod tigers-reunite -n project-tiger -o jsonpath='{.spec.nodeName}')

# Find the container ID and runtimeType on the node
# We use docker exec because kind nodes are docker containers
CONTAINER_ID=$(docker exec "$NODE" crictl ps --name tigers-reunite -q)
RUNTIME_TYPE=$(docker exec "$NODE" crictl inspect "$CONTAINER_ID" --template '{{.info.runtimeType}}')

# Write to pod-container.txt
mkdir -p "$SCRIPT_DIR/../lab"
echo "$CONTAINER_ID $RUNTIME_TYPE" > "$SCRIPT_DIR/../lab/pod-container.txt"

# Write logs to container.log
docker exec "$NODE" crictl logs "$CONTAINER_ID" > "$SCRIPT_DIR/../lab/container.log"
