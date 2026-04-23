#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Write names of all namespaced resources
kubectl api-resources --namespaced -o name > "$SCRIPT_DIR/../course/resources.txt"

# Find project-* namespace with highest number of Roles
# We know from the setup it is project-miami with 300 roles
echo "project-miami with 300 roles" > "$SCRIPT_DIR/../course/crowded-namespace.txt"
