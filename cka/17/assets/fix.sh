#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

# Create the Pod
kubectl -n project-tiger run tigers-reunite --image=httpd:2-alpine --labels "pod=container,container=pod"

# Wait for Pod to be running
kubectl -n project-tiger wait --for=condition=Ready pod/tigers-reunite --timeout=60s

# Find the node
NODE_NAME=$(kubectl -n project-tiger get pod tigers-reunite -o jsonpath='{.spec.nodeName}')

# Find container ID on that node
# We use docker exec to run crictl on the node
CONTAINER_ID=$(docker exec "$NODE_NAME" crictl ps --name tigers-reunite -q)

# Get runtimeType
RUNTIME_TYPE=$(docker exec "$NODE_NAME" crictl inspect "$CONTAINER_ID" | grep runtimeType | cut -d '"' -f 4)

# Write to pod-container.txt
echo "$CONTAINER_ID $RUNTIME_TYPE" > "$SCRIPT_DIR/../course/pod-container.txt"

# Get logs - capture both stdout and stderr
docker exec "$NODE_NAME" crictl logs "$CONTAINER_ID" > "$SCRIPT_DIR/../course/pod-container.log" 2>&1
