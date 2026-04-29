#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$SCRIPT_DIR/../lab"

# Only create cluster if it doesn't exist (helpful for local debugging)
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# Install metrics-server with kubelet-insecure-tls (required for kind)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch deployment metrics-server \
  -n kube-system \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

echo "Waiting for metrics-server to be ready..."
kubectl rollout status -n kube-system deployment/metrics-server --timeout=120s

# Seed resources
kubectl apply -f "$SCRIPT_DIR/workloads.yaml"

echo "Waiting for deployments to be ready..."
kubectl rollout status deployment api-gateway -n api-gateway-staging --timeout=120s
kubectl rollout status deployment api-gateway -n api-gateway-prod --timeout=120s

echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
