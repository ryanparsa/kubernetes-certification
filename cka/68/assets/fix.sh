#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prioritize existing KUBECONFIG (CI), fallback to local lab directory
if [ -z "${KUBECONFIG:-}" ]; then
  if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
    export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
  fi
fi

# Create Namespace
kubectl create namespace ci --dry-run=client -o yaml | kubectl apply -f -

# Create ServiceAccount
kubectl create serviceaccount cicd-sa -n ci --dry-run=client -o yaml | kubectl apply -f -

# Create Role
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: ci
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["create", "update", "delete"]
EOF

# Create RoleBinding
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cicd-sa-deployment-manager
  namespace: ci
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: deployment-manager
subjects:
- kind: ServiceAccount
  name: cicd-sa
  namespace: ci
EOF
