#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

LAB_DIR="$SCRIPT_DIR/../lab"
mkdir -p "$LAB_DIR"

# 1. Create a new Namespace called cka-master
kubectl create namespace cka-master --dry-run=client -o yaml | kubectl apply -f -

# 2. Write the names of all namespaced Kubernetes resources into lab/resources.txt
kubectl api-resources --namespaced -o name > "$LAB_DIR/resources.txt"

# 3. Find the project-* Namespace with the highest number of Roles and write its name and amount
MAX_ROLES=0
CROWDED_NS=""

for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep '^project-'); do
  COUNT=$(kubectl -n "$ns" get roles --no-headers 2>/dev/null | wc -l || echo 0)
  if [ "$COUNT" -gt "$MAX_ROLES" ]; then
    MAX_ROLES=$COUNT
    CROWDED_NS=$ns
  fi
done

if [ -n "$CROWDED_NS" ]; then
  echo "$CROWDED_NS with $MAX_ROLES roles" > "$LAB_DIR/crowded-namespace.txt"
fi
