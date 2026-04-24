#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"

kind delete cluster --name "$EXAM-lab-$LAB_ID" || true
rm -rf "$SCRIPT_DIR/../course"
echo "Lab torn down."
