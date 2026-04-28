#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  echo "Cluster $CLUSTER_NAME already exists."
  if [[ ! -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
  fi
fi

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# 3. Apply pre-existing workloads
# Create a dummy context
kubectl config set-context other-context --cluster="kind-$CLUSTER_NAME" --user="kind-$CLUSTER_NAME" --namespace=default

# 4. Wait for deployments
# N/A

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 6. Copy task assets
# N/A

# 7. Print summary
echo ""
echo "Lab ready!"
echo "Run: export KUBECONFIG=$SCRIPT_DIR/kubeconfig.yaml"
echo "Check nodes: kubectl get nodes"
