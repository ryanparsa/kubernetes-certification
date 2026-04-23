#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

kind delete cluster --name cka-lab

rm -rf "$SCRIPT_DIR/../course"

echo "Lab torn down."
