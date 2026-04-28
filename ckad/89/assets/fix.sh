#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Create ConfigMap
kubectl create configmap trauerweide --from-literal=tree=trauerweide --dry-run=client -o yaml | kubectl apply -f -

# Create Pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-6
  namespace: default
spec:
  containers:
  - name: pod-6
    image: busybox:1.31.0
    command: ["sleep", "999"]
    volumeMounts:
    - name: data
      mountPath: /tmp/vols
  volumes:
  - name: data
    emptyDir: {}
EOF

# Wait for pod to be ready
kubectl wait pod/pod-6 -n default --for=condition=Ready --timeout=60s
