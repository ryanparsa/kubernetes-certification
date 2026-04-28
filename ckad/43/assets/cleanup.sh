#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# tear down cluster
if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind delete cluster --name "$CLUSTER_NAME"
fi

rm -rf "$SCRIPT_DIR/../lab"
rm -f "$SCRIPT_DIR/kubeconfig.yaml"

echo "Lab torn down."
