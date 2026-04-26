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
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/workloads.yaml"

# 4. Wait for deployments
echo "Waiting for deployments in project-c13 to be ready..."
for deploy in c13-2x3-api c13-2x3-web c13-3cc-data c13-3cc-runner-heavy c13-3cc-web; do
  kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n project-c13 \
    deployment/"$deploy" --timeout=120s
done

# 5. Create the course/ output directory
mkdir -p "$SCRIPT_DIR/../course"

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
