#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
LAB_DIR="$(dirname "$SCRIPT_DIR")"
COURSE_DIR="$LAB_DIR/course"
CLUSTER_NAME="cka-lab-15"

mkdir -p "$COURSE_DIR"

# 1. Write the cluster_events.sh command
cat <<'EOF' > "$COURSE_DIR/cluster_events.sh"
kubectl get events -A --sort-by=.metadata.creationTimestamp
EOF
chmod +x "$COURSE_DIR/cluster_events.sh"

# 2. Delete the kube-proxy pod and record events
# Find the kube-proxy pod name on the control-plane node
KUBE_PROXY_POD=$(kubectl -n kube-system get pod -l k8s-app=kube-proxy -o jsonpath='{.items[0].metadata.name}')

kubectl -n kube-system delete pod "$KUBE_PROXY_POD" --now

# Wait a bit for events to be generated
sleep 5

# Record events to pod_kill.log
"$COURSE_DIR/cluster_events.sh" > "$COURSE_DIR/pod_kill.log"

# 3. Manually kill the containerd container of the kube-proxy pod
# Get the new kube-proxy pod name
NEW_KUBE_PROXY_POD=$(kubectl -n kube-system get pod -l k8s-app=kube-proxy -o jsonpath='{.items[0].metadata.name}')

# Get the container ID from inside the kind node
CONTAINER_ID=$(docker exec "$CLUSTER_NAME-control-plane" crictl ps --name kube-proxy -q | head -n 1)

# Kill the container
docker exec "$CLUSTER_NAME-control-plane" crictl rm --force "$CONTAINER_ID"

# Wait a bit for events
sleep 5

# Record events to container_kill.log
"$COURSE_DIR/cluster_events.sh" > "$COURSE_DIR/container_kill.log"
