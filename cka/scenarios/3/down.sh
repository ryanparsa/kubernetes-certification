#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
kind delete cluster --name cka-task-3 || true
rm -f "$DIR/kubeconfig"
echo "cluster cka-task-3 deleted"
