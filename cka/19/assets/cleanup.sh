#!/usr/bin/env bash
set -euo pipefail

# 2. Delete cluster
kind delete cluster --name cka-lab

# 5. Remove the course/ output directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf "$SCRIPT_DIR/../course"

echo "Lab torn down."
