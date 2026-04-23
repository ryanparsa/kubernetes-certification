#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create the Pod
kubectl -n project-hamster run p2-pod --image=nginx:1-alpine --labels="run=p2-pod"

# 2. Create the Service
kubectl -n project-hamster expose pod p2-pod --name p2-service --port 3000 --target-port 80

# Wait for Pod to be ready
kubectl -n project-hamster wait --for=condition=Ready pod/p2-pod --timeout=60s

# 3. Capture iptables rules
# Give kube-proxy a moment to sync rules
sleep 5
docker exec "$CLUSTER_NAME-control-plane" iptables-save | grep p2-service > "$SCRIPT_DIR/../course/iptables.txt" || true

# 4. Delete the Service
kubectl -n project-hamster delete svc p2-service
