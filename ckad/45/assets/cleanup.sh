#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind delete cluster --name "$CLUSTER_NAME"
fi

rm -rf "$TASK_DIR/lab"
echo "Lab torn down."
