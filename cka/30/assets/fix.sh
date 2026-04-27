#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multi-container-playground
  name: multi-container-playground
  namespace: default
spec:
  containers:
  - image: nginx:1-alpine
    name: c1
    resources: {}
    env:
    - name: MY_NODE_NAME
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
    volumeMounts:
    - name: vol
      mountPath: /vol
  - image: busybox:1
    name: c2
    command: ["sh", "-c", "while true; do date >> /vol/date.log; sleep 1; done"]
    volumeMounts:
    - name: vol
      mountPath: /vol
  - image: busybox:1
    name: c3
    command: ["sh", "-c", "tail -f /vol/date.log"]
    volumeMounts:
    - name: vol
      mountPath: /vol
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:
  - name: vol
    emptyDir: {}
EOF

kubectl wait pod multi-container-playground --for=condition=Ready --timeout=60s
