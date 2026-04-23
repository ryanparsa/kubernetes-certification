#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create the first Pod: ready-if-service-ready
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: ready-if-service-ready
  name: ready-if-service-ready
  namespace: default
spec:
  containers:
  - image: nginx:1-alpine
    name: ready-if-service-ready
    livenessProbe:
      exec:
        command:
        - 'true'
    readinessProbe:
      exec:
        command:
        - sh
        - -c
        - 'wget -T2 -O- http://service-am-i-ready:80'
  dnsPolicy: ClusterFirst
  restartPolicy: Always
EOF

# 2. Create the second Pod: am-i-ready
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    id: cross-server-ready
  name: am-i-ready
  namespace: default
spec:
  containers:
  - image: nginx:1-alpine
    name: am-i-ready
EOF

# 3. Wait for Pods to be Ready
kubectl wait pod ready-if-service-ready --for=condition=Ready --timeout=60s
kubectl wait pod am-i-ready --for=condition=Ready --timeout=60s
