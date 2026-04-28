#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
CP_NODE="${CLUSTER_NAME}-control-plane"

if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# 1. Stop the kube-scheduler by moving its static pod manifest out
docker exec "$CP_NODE" mv \
  /etc/kubernetes/manifests/kube-scheduler.yaml \
  /etc/kubernetes/kube-scheduler.yaml

echo "Waiting for kube-scheduler pod to disappear..."
kubectl wait pod -n kube-system -l component=kube-scheduler \
  --for=delete --timeout=60s 2>/dev/null || true

# 2. Create the first Pod - stays Pending without the scheduler
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: manual-schedule
  namespace: default
  labels:
    run: manual-schedule
spec:
  containers:
  - name: manual-schedule
    image: httpd:2-alpine
EOF

# 3. Manually schedule by re-creating the Pod with nodeName set
kubectl delete pod manual-schedule --ignore-not-found
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: manual-schedule
  namespace: default
  labels:
    run: manual-schedule
spec:
  nodeName: ${CP_NODE}
  containers:
  - name: manual-schedule
    image: httpd:2-alpine
  tolerations:
  - effect: NoSchedule
    operator: Exists
EOF

kubectl wait pod manual-schedule --for=condition=Ready --timeout=60s

# 4. Bring the scheduler back
docker exec "$CP_NODE" mv \
  /etc/kubernetes/kube-scheduler.yaml \
  /etc/kubernetes/manifests/kube-scheduler.yaml

echo "Waiting for kube-scheduler to restart..."
kubectl wait pod -n kube-system -l component=kube-scheduler \
  --for=condition=Ready --timeout=120s

# 5. Create a second Pod - the running scheduler places it on the worker
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: manual-schedule2
  namespace: default
  labels:
    run: manual-schedule2
spec:
  containers:
  - name: manual-schedule2
    image: httpd:2-alpine
EOF

kubectl wait pod manual-schedule2 --for=condition=Ready --timeout=60s
