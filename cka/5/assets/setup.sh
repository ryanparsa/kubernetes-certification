#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
CLUSTER_NAME="cka-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$SCRIPT_DIR/../lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Install metrics-server with kubelet-insecure-tls (required for kind)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" \
  -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch deployment metrics-server \
  --kubeconfig "$KUBECONFIG_FILE" \
  -n kube-system \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

echo "Waiting for metrics-server to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" \
  -n kube-system deployment/metrics-server --timeout=120s

# Create the lab/ directory and copy kustomize structure into it
cp -r "$SCRIPT_DIR/api-gateway" "$SCRIPT_DIR/../lab/api-gateway"

# Create the namespaces required by staging and prod overlays
kubectl create namespace api-gateway-staging --kubeconfig "$KUBECONFIG_FILE"
kubectl create namespace api-gateway-prod --kubeconfig "$KUBECONFIG_FILE"

# Deploy staging and prod using kustomize
kubectl kustomize "$SCRIPT_DIR/../lab/api-gateway/staging" \
  | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

kubectl kustomize "$SCRIPT_DIR/../lab/api-gateway/prod" \
  | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

echo "Waiting for deployments to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n api-gateway-staging \
  deployment/api-gateway --timeout=120s
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n api-gateway-prod \
  deployment/api-gateway --timeout=120s

echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
