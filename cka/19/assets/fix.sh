#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# 1. Create the Static Pod manifest on the control-plane node
# We use docker exec to write the file directly to /etc/kubernetes/manifests/
# Static Pods are automatically picked up by the kubelet.
docker exec "$CLUSTER_NAME-control-plane" bash -c "cat <<EOF > /etc/kubernetes/manifests/19.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: my-static-pod
  name: my-static-pod
spec:
  containers:
  - image: nginx:1-alpine
    name: my-static-pod
    resources:
      requests:
        cpu: 10m
        memory: 20Mi
EOF"

# 2. Wait for the Static Pod to be created and running
# The name of the static pod will be my-static-pod-<node-name>
STATIC_POD_NAME="my-static-pod-$CLUSTER_NAME-control-plane"

echo "Waiting for Static Pod $STATIC_POD_NAME to be Running..."
until kubectl get pod "$STATIC_POD_NAME" -n default &>/dev/null; do
    sleep 2
done
kubectl wait pod "$STATIC_POD_NAME" -n default --for=condition=Ready --timeout=60s

# 3. Create the NodePort Service
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  labels:
    run: my-static-pod
  name: static-pod-service
  namespace: default
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: my-static-pod
  type: NodePort
EOF
