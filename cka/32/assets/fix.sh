#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# Use local kubeconfig if it exists, otherwise assume it's already set (e.g. in CI)
if [[ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# 1. Create cluster_events.sh
mkdir -p "$SCRIPT_DIR/../lab"
cat <<EOF > "$SCRIPT_DIR/../lab/cluster_events.sh"
kubectl get events -A --sort-by=.metadata.creationTimestamp
EOF
chmod +x "$SCRIPT_DIR/../lab/cluster_events.sh"

# 2. Delete kube-proxy pod and capture logs
# Wait for pods to be ready first to ensure we have a kube-proxy pod
kubectl wait --for=condition=Ready pods -l k8s-app=kube-proxy -n kube-system --timeout=60s

POD_NAME=$(kubectl -n kube-system get pod -l k8s-app=kube-proxy -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system delete pod "$POD_NAME" --wait=false

# Give it some time to generate events
sleep 5

bash "$SCRIPT_DIR/../lab/cluster_events.sh" > "$SCRIPT_DIR/../lab/pod_kill.log"

# 3. Kill kube-proxy container and capture logs
# Wait for the new pod to be ready
kubectl wait --for=condition=Ready pods -l k8s-app=kube-proxy -n kube-system --timeout=60s

# Get the container ID from the node
# We use docker exec because crictl is inside the node
CONTAINER_ID=$(docker exec "$CLUSTER_NAME-control-plane" crictl ps --name kube-proxy -q | head -n 1)

docker exec "$CLUSTER_NAME-control-plane" crictl rm --force "$CONTAINER_ID"

# Give it some time to generate events
sleep 5

bash "$SCRIPT_DIR/../lab/cluster_events.sh" > "$SCRIPT_DIR/../lab/container_kill.log"
