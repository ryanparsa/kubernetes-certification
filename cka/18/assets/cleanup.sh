#!/usr/bin/env bash
set -euo pipefail

kind delete cluster --name cka-lab

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf "$SCRIPT_DIR/../lab"

echo "Lab torn down."
