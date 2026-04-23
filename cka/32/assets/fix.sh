#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create cluster_events.sh
mkdir -p "$SCRIPT_DIR/../course"
cat <<EOF > "$SCRIPT_DIR/../course/cluster_events.sh"
kubectl get events -A --sort-by=.metadata.creationTimestamp
EOF
chmod +x "$SCRIPT_DIR/../course/cluster_events.sh"

# 2. Delete kube-proxy pod and capture logs
# Wait for pods to be ready first to ensure we have a kube-proxy pod
kubectl wait --for=condition=Ready pods -l k8s-app=kube-proxy -n kube-system --timeout=60s

POD_NAME=$(kubectl -n kube-system get pod -l k8s-app=kube-proxy -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system delete pod "$POD_NAME" --wait=false

# Give it some time to generate events
sleep 5

bash "$SCRIPT_DIR/../course/cluster_events.sh" > "$SCRIPT_DIR/../course/pod_kill.log"

# 3. Kill kube-proxy container and capture logs
# Wait for the new pod to be ready
kubectl wait --for=condition=Ready pods -l k8s-app=kube-proxy -n kube-system --timeout=60s

# Get the container ID from the node
# We use docker exec because crictl is inside the node
CONTAINER_ID=$(docker exec cka-lab-32-control-plane crictl ps --name kube-proxy -q | head -n 1)

docker exec cka-lab-32-control-plane crictl rm --force "$CONTAINER_ID"

# Give it some time to generate events
sleep 5

bash "$SCRIPT_DIR/../course/cluster_events.sh" > "$SCRIPT_DIR/../course/container_kill.log"
