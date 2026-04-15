#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

# Create cluster with 2 worker nodes
cat <<EOF > "$DIR/kind-config.yaml"
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF

kind create cluster --name cka-task-19 --kubeconfig "$KUBECONFIG" --config "$DIR/kind-config.yaml"

# Deploy a "legacy-app" and force it to worker1
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legacy-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: legacy
  template:
    metadata:
      labels:
        app: legacy
    spec:
      nodeName: cka-task-19-worker
      containers:
      - name: nginx
        image: nginx:1.27-alpine
EOF
kubectl wait --for=condition=available deployment/legacy-app --timeout=60s
