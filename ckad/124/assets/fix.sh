#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

kubectl create serviceaccount secret-manager -n sun --dry-run=client -o yaml | kubectl apply -f -

kubectl create rolebinding secret-manager \
  --clusterrole=secret-manager \
  --serviceaccount=sun:secret-manager \
  -n sun \
  --dry-run=client -o yaml | kubectl apply -f -
