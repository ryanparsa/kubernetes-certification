#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-27 --kubeconfig "$KUBECONFIG"

kubectl create ns quota-test

# Apply a resource quota that limits pods to 2
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: pod-quota
  namespace: quota-test
spec:
  hard:
    pods: "2"
EOF

# Deploy a deployment with 5 replicas (it will only scale to 2)
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: limited-app
  namespace: quota-test
spec:
  replicas: 5
  selector:
    matchLabels:
      app: limited
  template:
    metadata:
      labels:
        app: limited
    spec:
      containers:
      - name: nginx
        image: nginx:1.27-alpine
EOF

echo "Deployment 'limited-app' created in namespace 'quota-test' with restrictive quota."
