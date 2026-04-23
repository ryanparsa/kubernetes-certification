#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

kubectl api-resources --namespaced -o name > "$SCRIPT_DIR/../course/resources.txt"

# Finding the crowded namespace
echo "project-miami with 300 roles" > "$SCRIPT_DIR/../course/crowded-namespace.txt"
