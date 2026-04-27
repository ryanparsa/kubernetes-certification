#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# 1. Create static pod manifest on the control-plane node
docker exec "${CLUSTER_NAME}-control-plane" bash -c 'cat > /etc/kubernetes/manifests/my-static-pod.yaml <<'"'"'EOF'"'"'
apiVersion: v1
kind: Pod
metadata:
  name: my-static-pod
  namespace: default
  labels:
    run: my-static-pod
spec:
  containers:
  - name: my-static-pod
    image: nginx:1-alpine
    resources:
      requests:
        cpu: 10m
        memory: 20Mi
EOF'

# 2. Wait for the static pod to appear and be Ready
kubectl wait pod "my-static-pod-${CLUSTER_NAME}-control-plane" \
  --for=condition=Ready --timeout=60s

# 3. Create the NodePort Service
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: static-pod-service
  namespace: default
  labels:
    run: my-static-pod
spec:
  type: NodePort
  selector:
    run: my-static-pod
  ports:
  - port: 80
    targetPort: 80
EOF
