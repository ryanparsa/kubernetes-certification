#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# Create cluster if it doesn't exist
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  # If it exists, we might be in CI where kind-action already created it
  # Ensure we have a kubeconfig file at the expected location
  if [ ! -f "$KUBECONFIG_FILE" ]; then
    kind export kubeconfig --name "$CLUSTER_NAME" --kubeconfig "$KUBECONFIG_FILE"
  fi
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# Create namespace
kubectl create namespace neptune --dry-run=client -o yaml | kubectl apply -f -

# Create deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-new-c32
  namespace: neptune
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-new-c32
  template:
    metadata:
      labels:
        app: api-new-c32
    spec:
      containers:
      - name: httpd
        image: httpd:2.4.39-alpine
EOF

# Wait for deployment
if ! kubectl rollout status deployment/api-new-c32 -n neptune --timeout=300s; then
  echo "Deployment failed to roll out. Debug info:"
  kubectl describe deployment api-new-c32 -n neptune
  kubectl get pods -n neptune
  kubectl describe pods -n neptune
  exit 1
fi

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
