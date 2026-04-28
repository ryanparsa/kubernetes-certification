#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Create ServiceAccount
kubectl -n project-hamster create sa processor

# Create Role
kubectl -n project-hamster create role processor --verb=create --resource=secrets,configmaps

# Create RoleBinding
kubectl -n project-hamster create rolebinding processor --role=processor --serviceaccount=project-hamster:processor
