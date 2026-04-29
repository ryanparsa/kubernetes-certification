#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="${KUBECONFIG:-$SCRIPT_DIR/../lab/kubeconfig.yaml}"
export KUBECONFIG="$KUBECONFIG_FILE"

# 1. Create namespaces
for ns in project-jinan project-miami project-melbourne project-seoul project-toronto; do
  kubectl create namespace "$ns" --dry-run=client -o yaml | kubectl apply -f -
done

# 2. Seed roles
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
  kubectl create role role-$i --namespace project-seoul --verb=get --resource=pods --dry-run=client -o yaml | kubectl apply -f -
done

# project-melbourne gets 2 roles
echo "Seeding 2 roles into project-melbourne..."
kubectl create role role-1 --namespace project-melbourne --verb=get --resource=pods --dry-run=client -o yaml | kubectl apply -f -
kubectl create role role-2 --namespace project-melbourne --verb=get --resource=pods --dry-run=client -o yaml | kubectl apply -f -

# 3. Wait for CoreDNS
echo "Waiting for CoreDNS to be ready..."
kubectl rollout status -n kube-system deployment/coredns --timeout=120s
