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
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

export KUBECONFIG="$KUBECONFIG_FILE"

# 3. Create namespaces
for ns in project-jinan project-miami project-melbourne project-seoul project-toronto; do
  kubectl create namespace "$ns"
done

# 4. Seed roles
# project-miami gets 300 roles - use a temporary file for speed
echo "Seeding 300 roles into project-miami..."
ROLES_FILE=$(mktemp)
for i in $(seq 1 300); do
  echo "---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-$i
  namespace: project-miami
rules: []" >> "$ROLES_FILE"
done
kubectl apply -f "$ROLES_FILE"
rm "$ROLES_FILE"

# project-seoul gets 10 roles
echo "Seeding 10 roles into project-seoul..."
for i in $(seq 1 10); do
  kubectl create role role-$i --namespace project-seoul --verb=get --resource=pods
done

# project-melbourne gets 2 roles
echo "Seeding 2 roles into project-melbourne..."
kubectl create role role-1 --namespace project-melbourne --verb=get --resource=pods
kubectl create role role-2 --namespace project-melbourne --verb=get --resource=pods

# 5. Wait for CoreDNS
echo "Waiting for CoreDNS to be ready..."
kubectl rollout status -n kube-system deployment/coredns --timeout=120s

# 6. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
