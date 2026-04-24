#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

mkdir -p "$SCRIPT_DIR/../course"

# SEEDING (Idempotent)
# Ensure project-* namespaces exist
kubectl apply -f "$SCRIPT_DIR/namespaces.yaml"

# Create Roles in project-miami (300), project-melbourne (2), project-seoul (10)
for ns_count in "project-miami:300" "project-melbourne:2" "project-seoul:10"; do
  ns="${ns_count%%:*}"
  count="${ns_count##*:}"
  {
    for i in $(seq 1 "$count"); do
      cat <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-$i
  namespace: $ns
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get"]
---
EOF
    done
  } | kubectl apply -f -
done

# SOLUTION
# 1. write all namespaced resource names to resources.txt
kubectl api-resources --namespaced -o name > "$SCRIPT_DIR/../course/resources.txt"

# 2. find the project-* namespace with the most Roles
max_count=0
max_ns=""
for ns in $(kubectl get namespace -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep '^project-'); do
  count=$(kubectl get role -n "$ns" --no-headers 2>/dev/null | wc -l | tr -d ' ')
  if [ "$count" -gt "$max_count" ]; then
    max_count=$count
    max_ns=$ns
  fi
done

echo "$max_ns with $max_count roles" > "$SCRIPT_DIR/../course/crowded-namespace.txt"
