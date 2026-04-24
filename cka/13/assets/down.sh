#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# Only delete cluster if it exists
if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind delete cluster --name "$CLUSTER_NAME"
fi

rm -rf "$SCRIPT_DIR/../course"
echo "Lab torn down."
