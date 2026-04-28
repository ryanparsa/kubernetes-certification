#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
CP_NODE="${CLUSTER_NAME}-control-plane"

KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Apply the solution
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pod
  namespace: default
spec:
  nodeName: ${CP_NODE}
  containers:
  - name: pod-container
    image: httpd:2.4.41-alpine
EOF

kubectl wait pod pod --for=condition=Ready --timeout=60s
