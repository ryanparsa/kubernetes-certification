#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"

# 1. Delete cluster
kind delete cluster --name "cka-lab-$LAB_ID"

# 2. Cleanup host data
rm -rf /tmp/cka6-data

# 3. Cleanup course directory
rm -rf "$SCRIPT_DIR/../course"

echo "Lab torn down."
