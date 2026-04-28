#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# Create cluster if not already in CI (which uses kind-action)
if ! kubectl cluster-info &>/dev/null; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Seed resources
kubectl create namespace sun --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace moon --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-manager
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
EOF

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready!"
