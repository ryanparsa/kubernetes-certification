#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

mkdir -p "$SCRIPT_DIR/../lab"

cat <<EOF > "$SCRIPT_DIR/../lab/node-monitor.yaml"
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-monitor
  namespace: default
  labels:
    app: node-monitor
spec:
  selector:
    matchLabels:
      app: node-monitor
  template:
    metadata:
      labels:
        app: node-monitor
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      nodeSelector:
        kubernetes.io/os: linux
      containers:
      - name: monitor
        image: busybox
        command:
        - sh
        - -c
        - 'while true; do echo "Node: \$(hostname)"; sleep 30; done'
        resources:
          requests:
            cpu: 50m
            memory: 32Mi
EOF

kubectl apply -f "$SCRIPT_DIR/../lab/node-monitor.yaml"
kubectl rollout status daemonset/node-monitor --timeout=60s
