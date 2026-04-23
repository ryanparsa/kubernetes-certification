#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pod1
  namespace: default
spec:
  containers:
  - name: pod1-container
    image: httpd:2-alpine
  tolerations:
  - effect: NoSchedule
    key: node-role.kubernetes.io/control-plane
  nodeSelector:
    node-role.kubernetes.io/control-plane: ""
EOF

kubectl wait pod pod1 -n default --for=condition=Ready --timeout=60s
