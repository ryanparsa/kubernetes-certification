#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# Provision cluster if it doesn't exist
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# Seed resources
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: neptune
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neptune-10ab
  namespace: neptune
  labels:
    app: neptune-10ab
spec:
  replicas: 3
  selector:
    matchLabels:
      app: neptune-10ab
  template:
    metadata:
      labels:
        app: neptune-10ab
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neptune-20ab
  namespace: neptune
  labels:
    app: neptune-20ab
spec:
  replicas: 2
  selector:
    matchLabels:
      app: neptune-20ab
  template:
    metadata:
      labels:
        app: neptune-20ab
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
EOF

# Wait for deployments
kubectl wait deployment neptune-10ab -n neptune --for=condition=Available --timeout=60s
kubectl wait deployment neptune-20ab -n neptune --for=condition=Available --timeout=60s

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
