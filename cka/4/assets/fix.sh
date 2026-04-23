#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

mkdir -p "$SCRIPT_DIR/../course"

kubectl get pods -n project-c13 \
  -o jsonpath="{range .items[?(@.status.qosClass=='BestEffort')]}{.metadata.name}{'\n'}{end}" \
  > "$SCRIPT_DIR/../course/pods-terminated-first.txt"
