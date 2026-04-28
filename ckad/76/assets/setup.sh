#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
mkdir -p "$TASK_DIR/lab"
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
fi

# 3. Wait for nodes to be ready
kubectl --kubeconfig "$KUBECONFIG_FILE" wait --for=condition=Ready nodes --all --timeout=120s

# 4. Seed the app-stack namespace and pods
kubectl --kubeconfig "$KUBECONFIG_FILE" create namespace app-stack --dry-run=client -o yaml | \
  kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f -

kubectl --kubeconfig "$KUBECONFIG_FILE" apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: app-stack
  labels:
    app: todo
    tier: frontend
spec:
  containers:
  - name: frontend
    image: nginx:stable-alpine
---
apiVersion: v1
kind: Pod
metadata:
  name: backend
  namespace: app-stack
  labels:
    app: todo
    tier: backend
spec:
  containers:
  - name: backend
    image: nginx:stable-alpine
---
apiVersion: v1
kind: Pod
metadata:
  name: database
  namespace: app-stack
  labels:
    app: todo
    tier: database
spec:
  containers:
  - name: database
    image: nginx:stable-alpine
EOF

kubectl --kubeconfig "$KUBECONFIG_FILE" wait pod/frontend pod/backend pod/database \
  -n app-stack --for=condition=Ready --timeout=120s

# 5. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
