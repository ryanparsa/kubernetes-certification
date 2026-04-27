#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
mkdir -p "$SCRIPT_DIR/../lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/namespaces.yaml"

echo "Creating Roles in project-miami (300)..."
{
  for i in $(seq 1 300); do
    cat <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-$i
  namespace: project-miami
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get"]
---
EOF
  done
} | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

echo "Creating Roles in project-melbourne (2)..."
{
  for i in $(seq 1 2); do
    cat <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-$i
  namespace: project-melbourne
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get"]
---
EOF
  done
} | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

echo "Creating Roles in project-seoul (10)..."
{
  for i in $(seq 1 10); do
    cat <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-$i
  namespace: project-seoul
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get"]
---
EOF
  done
} | kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f -

# 5. Create the lab/ output directory

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
