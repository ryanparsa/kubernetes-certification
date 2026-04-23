#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_KUBECONFIG="$SCRIPT_DIR/../course/kubeconfig"

# Step 1: Write all context names (one per line)
kubectl config get-contexts -o name --kubeconfig "$TASK_KUBECONFIG" \
  > "$SCRIPT_DIR/../course/contexts"

# Step 2: Write the current context
kubectl config current-context --kubeconfig "$TASK_KUBECONFIG" \
  > "$SCRIPT_DIR/../course/current-context"

# Step 3: Extract and base64-decode the client certificate for account-0027
kubectl config view --raw --kubeconfig "$TASK_KUBECONFIG" \
  -o jsonpath="{.users[?(@.name=='account-0027@internal')].user.client-certificate-data}" \
  | base64 -d > "$SCRIPT_DIR/../course/cert"
