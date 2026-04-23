#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"

kind delete cluster --name "cka-lab-$LAB_ID"

echo "Lab torn down."
