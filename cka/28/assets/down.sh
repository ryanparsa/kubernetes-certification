#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# 1. Delete cluster
kind delete cluster --name "$CLUSTER_NAME"

# 2. Clean up course directory
rm -rf "$SCRIPT_DIR/../course"

echo "Lab torn down."
