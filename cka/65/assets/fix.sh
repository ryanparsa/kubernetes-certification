#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Ensure /tmp/exam exists
mkdir -p /tmp/exam

# Ensure namespace exists (in case setup.sh wasn't run, e.g. in CI)
kubectl create namespace upgrade --dry-run=client -o yaml | kubectl apply -f -

# 1. Create initial deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v1
  namespace: upgrade
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: app-v1
  template:
    metadata:
      labels:
        app: app-v1
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
EOF

kubectl wait deployment app-v1 -n upgrade --for=condition=Available --timeout=60s

# 2. Perform rolling update
kubectl set image deployment/app-v1 nginx=nginx:1.20 -n upgrade
kubectl rollout status deployment/app-v1 -n upgrade

# 3. Save rollout history
kubectl rollout history deployment app-v1 -n upgrade > /tmp/exam/rollout-history.txt

# 4. Roll back
kubectl rollout undo deployment/app-v1 -n upgrade
kubectl rollout status deployment/app-v1 -n upgrade
