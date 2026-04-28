#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Add Bitnami Helm repository (idempotent)
helm repo add bitnami https://charts.bitnami.com/bitnami || true
helm repo update

# Create namespace (idempotent)
kubectl create namespace web --dry-run=client -o yaml | kubectl apply -f -

# Install or upgrade nginx chart with 2 replicas (idempotent)
helm upgrade --install nginx bitnami/nginx \
  --namespace web \
  --set replicaCount=2

kubectl rollout status deployment/nginx -n web --timeout=120s
