#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Rolling update to httpd:2.4.41-alpine
kubectl set image deployment/api-new-c32 httpd=httpd:2.4.41-alpine -n neptune

# Wait for rollout
kubectl rollout status deployment/api-new-c32 -n neptune --timeout=60s

# 2. Roll back to original image
kubectl rollout undo deployment/api-new-c32 -n neptune

# Wait for rollback
kubectl rollout status deployment/api-new-c32 -n neptune --timeout=60s
