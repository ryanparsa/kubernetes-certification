#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-21 --kubeconfig "$KUBECONFIG"

# Deploy pod writing logs to a file
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: default
spec:
  containers:
  - name: main
    image: busybox:1.36
    command: ["/bin/sh", "-c", "while true; do echo \"\$(date) - processing job\" >> /var/log/app.log; sleep 5; done"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
  volumes:
  - name: logs
    emptyDir: {}
EOF
kubectl wait --for=condition=Ready pod/app --timeout=60s
