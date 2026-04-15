#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
kind delete cluster --name cka-task-N || true
rm -f "$DIR/assets/kubeconfig"
echo "cluster cka-task-N deleted"
