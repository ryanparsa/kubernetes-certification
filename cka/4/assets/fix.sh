#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

mkdir -p "$SCRIPT_DIR/../lab"

kubectl get pods -n project-c13 \
  -o jsonpath="{range .items[?(@.status.qosClass=='BestEffort')]}{.metadata.name}{'\n'}{end}" \
  > "$SCRIPT_DIR/../lab/pods-terminated-first.txt"
