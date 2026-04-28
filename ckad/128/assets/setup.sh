#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Provision cluster if it doesn't exist
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# 2. Create namespace
kubectl create namespace pluto --dry-run=client -o yaml | kubectl apply -f -

# 3. Deploy initial deployment with the volume as per description "existing volume named log-data"
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pluto-deployment
  namespace: pluto
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pluto-app
  template:
    metadata:
      labels:
        app: pluto-app
    spec:
      containers:
      - name: pluto-app
        image: nginx:1.25.3
      volumes:
      - name: log-data
        emptyDir: {}
EOF

# 4. Wait for deployment
kubectl wait deployment pluto-deployment -n pluto --for=condition=Available --timeout=60s

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
