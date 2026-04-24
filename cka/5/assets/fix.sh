#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/kubeconfig.yaml" ] && [ -z "${KUBECONFIG:-}" ]; then
  export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
fi

COURSE_DIR="$SCRIPT_DIR/../course"
mkdir -p "$COURSE_DIR"

echo "kubectl get pod -A --sort-by=.metadata.creationTimestamp" > "$COURSE_DIR/find_pods.sh"
echo "kubectl get pod -A --sort-by=.metadata.uid" > "$COURSE_DIR/find_pods_uid.sh"

chmod +x "$COURSE_DIR/find_pods.sh" "$COURSE_DIR/find_pods_uid.sh"
