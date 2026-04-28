#!/usr/bin/env bash
set -euo pipefail

# 1. Check dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$LAB_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

# 3. Apply pre-existing workloads
if [[ -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# We need to ensure the networking namespace exists if it's supposed to be pre-seeded or if the user is supposed to create it.
# The prompt says "Create a Kubernetes Job ... in the networking namespace".
# Usually, if the namespace is not mentioned as "create it", it might be expected to exist.
# But looking at answer.md, it includes "kubectl create namespace networking".
# To be safe, I won't create it here unless I want to simulate an existing environment.

# 4. Wait for deployments
# N/A

# 5. Create the output directory
mkdir -p "$LAB_DIR/lab"

# 6. Copy task assets
# N/A

# 7. Print summary
echo "Lab ready! Run: export KUBECONFIG=$(realpath "$KUBECONFIG_FILE")"
echo "To access the control-plane node: docker exec -it $CLUSTER_NAME-control-plane bash"
