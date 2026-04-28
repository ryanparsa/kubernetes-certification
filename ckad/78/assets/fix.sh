#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

# 1. Create the Deployment with label tier=backend and pod template label app=v1
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    tier: backend
  name: deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: v1
  template:
    metadata:
      labels:
        app: v1
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
EOF

kubectl rollout status deployment/deploy --timeout=60s

# 2. Update the container image to nginx:latest
kubectl set image deployment/deploy nginx=nginx:latest
kubectl rollout status deployment/deploy --timeout=60s

# 3. Scale the Deployment to 5 replicas
kubectl scale deployment/deploy --replicas=5
kubectl rollout status deployment/deploy --timeout=60s

# 4. Roll back to revision 1
kubectl rollout undo deployment/deploy --to-revision=1
kubectl rollout status deployment/deploy --timeout=60s
