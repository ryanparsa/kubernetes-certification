#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [[ -f "$SCRIPT_DIR/kubeconfig.yaml" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
fi

kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: project-tiger
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ds-important
  namespace: project-tiger
  labels:
    id: ds-important
    uuid: 18426a0b-5f59-4e10-923f-c0e078e82462
spec:
  selector:
    matchLabels:
      id: ds-important
      uuid: 18426a0b-5f59-4e10-923f-c0e078e82462
  template:
    metadata:
      labels:
        id: ds-important
        uuid: 18426a0b-5f59-4e10-923f-c0e078e82462
    spec:
      containers:
      - image: httpd:2-alpine
        name: ds-important
        resources:
          requests:
            cpu: 10m
            memory: 10Mi
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/control-plane
EOF

kubectl rollout status daemonset ds-important -n project-tiger --timeout=120s
