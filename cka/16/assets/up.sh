#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 4. Wait for deployments
echo "Waiting for CoreDNS to be ready..."
kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n kube-system deployment/coredns --timeout=120s

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

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 7. Print summary — always use export style, never --kubeconfig
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
