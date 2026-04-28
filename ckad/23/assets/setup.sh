#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
mkdir -p "$TASK_DIR/lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

export KUBECONFIG="$KUBECONFIG_FILE"

# 3. Seed the broken scenario: pod without resource limits
kubectl create namespace troubleshooting

# Wait for default service account to be provisioned by the controller
until kubectl get serviceaccount default -n troubleshooting --no-headers 2>/dev/null | grep -q default; do
  sleep 1
done

kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: logging-pod
  namespace: troubleshooting
spec:
  containers:
  - name: log-collector
    image: nginx:alpine
  - name: log-processor
    image: busybox:1.36
    command: ["sh", "-c", "while true; do echo processing; sleep 1; done"]
EOF

kubectl wait pod logging-pod -n troubleshooting --for=condition=Ready --timeout=120s

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
