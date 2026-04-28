#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Implement the solution
# Ensure the directory exists (should be handled by setup.sh but being idempotent/safe)
mkdir -p /opt/course/1 2>/dev/null || sudo mkdir -p /opt/course/1
sudo chmod 777 /opt/course/1 2>/dev/null || true

kubectl get namespaces -o name > /opt/course/1/namespaces
