#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$TASK_DIR/lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Install metrics-server with --kubelet-insecure-tls (required for kind)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch deployment metrics-server \
  --kubeconfig "$KUBECONFIG_FILE" \
  -n kube-system \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

echo "Waiting for metrics-server deployment to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" \
  -n kube-system deployment/metrics-server --timeout=120s

echo "Waiting for node metrics to become available..."
METRICS_READY=0
for i in $(seq 1 30); do
  if kubectl --kubeconfig "$KUBECONFIG_FILE" top node &>/dev/null; then
    echo "Metrics available."
    METRICS_READY=1
    break
  fi
  echo "  Attempt $i/30 - metrics not yet available, retrying in 10s..."
  sleep 10
done
if [ "$METRICS_READY" -eq 0 ]; then
  echo "Error: metrics-server did not become available after 300s"
  exit 1
fi

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
