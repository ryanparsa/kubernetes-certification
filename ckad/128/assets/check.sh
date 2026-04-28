#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"
python3 "$SCRIPT_DIR/_check.py"
