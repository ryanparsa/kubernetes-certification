#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"

CP_NAME="$EXAM-lab-$LAB_ID-cp"
WORKER_NAME="$EXAM-lab-$LAB_ID-worker"

limactl delete --force "$CP_NAME" "$WORKER_NAME" 2>/dev/null || true
rm -rf "$TASK_DIR/lab"

echo "Lab $LAB_ID cleaned up."
