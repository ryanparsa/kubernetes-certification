#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Fix 1 -- Correct the image
kubectl set image deployment/broken-deployment nginx=nginx:1.19 -n troubleshooting

# Fix 2 -- Relax resource constraints
kubectl patch deployment broken-deployment -n troubleshooting \
  --patch '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"cpu":"100m","memory":"128Mi"},"limits":{"cpu":"200m","memory":"256Mi"}}}]}}}}'

# Wait for rollout
kubectl rollout status deployment/broken-deployment -n troubleshooting --timeout=60s
