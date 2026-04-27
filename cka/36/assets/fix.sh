#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# 1. Create Pod
kubectl -n project-hamster run p2-pod --image=nginx:1-alpine
kubectl wait pod p2-pod -n project-hamster --for=condition=Ready --timeout=60s

# 2. Create Service
kubectl -n project-hamster expose pod p2-pod --name p2-service --port 3000 --target-port 80

# 3. Capture iptables
# Short sleep to ensure iptables rules are synced
sleep 5
docker exec "$CLUSTER_NAME-control-plane" iptables-save | grep p2-service > "$SCRIPT_DIR/../lab/iptables.txt"

# 4. Delete Service
kubectl -n project-hamster delete svc p2-service
