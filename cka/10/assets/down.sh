#!/usr/bin/env bash
set -euo pipefail

# Delete the kind cluster
kind delete cluster --name cka-lab

# Clean up course directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf "$SCRIPT_DIR/../course"

echo "Lab torn down."
