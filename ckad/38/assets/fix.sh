#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: multi-container
---
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  namespace: multi-container
spec:
  containers:
  - name: main-container
    image: nginx
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  - name: sidecar-container
    image: busybox
    command: ['sh', '-c', 'while true; do echo \$(date) >> /var/log/app.log; sleep 5; done']
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  volumes:
  - name: log-volume
    emptyDir: {}
EOF

kubectl wait --for=condition=Ready pod/multi-container-pod -n multi-container --timeout=60s
