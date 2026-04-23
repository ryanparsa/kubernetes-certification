#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create the Pod
kubectl -n project-hamster run p2-pod --image=nginx:1-alpine
kubectl wait pod p2-pod -n project-hamster --for=condition=Ready --timeout=60s

# 2. Create the Service
kubectl -n project-hamster expose pod p2-pod --name p2-service --port 3000 --target-port 80

# 3. Save the iptables rules to cka/36/course/iptables.txt
# Note: we need to wait a bit for kube-proxy to sync the rules
sleep 5
docker exec cka-lab-control-plane iptables-save | grep p2-service > "$SCRIPT_DIR/../course/iptables.txt" || true

# 4. Delete the Service
kubectl -n project-hamster delete svc p2-service
