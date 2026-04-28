#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"
if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# 1. Backup CoreDNS ConfigMap
# In the real exam, the student would run this on the control-plane node.
# Here we simulate it by using docker exec.
docker exec "${CLUSTER_NAME}-control-plane" mkdir -p /opt/course/95
docker exec "${CLUSTER_NAME}-control-plane" sh -c "kubectl -n kube-system get cm coredns -o yaml > /opt/course/95/coredns-backup.yaml"

# 2. Update CoreDNS configuration
# Forward very-secure.io to 1.2.3.4
kubectl -n kube-system get cm coredns -o json | jq '.data.Corefile |= . + "\nvery-secure.io:53 {\n    forward . 1.2.3.4\n}\n"' | kubectl apply -f -

# 3. Restart CoreDNS
kubectl -n kube-system rollout restart deployment coredns
kubectl -n kube-system rollout status deployment coredns --timeout=60s
