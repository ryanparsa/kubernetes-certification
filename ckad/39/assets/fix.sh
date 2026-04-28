#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

mkdir -p "$SCRIPT_DIR/../lab"

cat <<EOF > "$SCRIPT_DIR/../lab/39.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: pod-design
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: pod-design
  labels:
    app: frontend
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      tier: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:1.19.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-svc
  namespace: pod-design
spec:
  selector:
    app: frontend
    tier: frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
EOF

kubectl apply -f "$SCRIPT_DIR/../lab/39.yaml"
kubectl rollout status deployment/frontend -n pod-design --timeout=60s
