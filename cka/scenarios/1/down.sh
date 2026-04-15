#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
kind delete cluster --name cka-task-1 || true
rm -f "$DIR/assets/kubeconfig"
echo "cluster cka-task-1 deleted"
