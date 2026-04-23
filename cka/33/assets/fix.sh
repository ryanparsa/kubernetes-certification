#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Write the names of all namespaced Kubernetes resources
kubectl api-resources --namespaced -o name > "$SCRIPT_DIR/../course/resources.txt"

# Find the project-* Namespace with the highest number of Roles
MAX_ROLES=-1
CROWDED_NS=""

for ns in $(kubectl get namespaces -o name | grep 'project-'); do
  NS_NAME=$(basename "$ns")
  ROLE_COUNT=$(kubectl -n "$NS_NAME" get roles --no-headers 2>/dev/null | wc -l || echo 0)
  if [ "$ROLE_COUNT" -gt "$MAX_ROLES" ]; then
    MAX_ROLES=$ROLE_COUNT
    CROWDED_NS=$NS_NAME
  fi
done

echo "$CROWDED_NS with $MAX_ROLES roles" > "$SCRIPT_DIR/../course/crowded-namespace.txt"
