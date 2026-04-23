#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
CLUSTER_NAME="cka-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
export KUBECONFIG="$KUBECONFIG_FILE"

# Install metrics-server with kubelet-insecure-tls (required for kind)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch deployment metrics-server \
  -n kube-system \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

# Create the namespaces required by staging and prod overlays
kubectl create namespace api-gateway-staging
kubectl create namespace api-gateway-prod

# Deploy staging and prod using kustomize
kubectl kustomize "$SCRIPT_DIR/api-gateway/staging" | kubectl apply -f -
kubectl kustomize "$SCRIPT_DIR/api-gateway/prod" | kubectl apply -f -

# 4. Wait for deployments
echo "Waiting for metrics-server to be ready..."
kubectl rollout status -n kube-system deployment/metrics-server --timeout=120s

echo "Waiting for api-gateway deployments to be ready..."
kubectl rollout status -n api-gateway-staging deployment/api-gateway --timeout=120s
kubectl rollout status -n api-gateway-prod deployment/api-gateway --timeout=120s

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"
cp -r "$SCRIPT_DIR/api-gateway" "$SCRIPT_DIR/../course/api-gateway"

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
