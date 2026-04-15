#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
kind delete cluster --name cka-task-16 || true
rm -f "$DIR/kubeconfig"
echo "cluster cka-task-16 deleted"
