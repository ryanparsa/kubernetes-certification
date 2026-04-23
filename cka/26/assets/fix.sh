#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Stop scheduler
docker exec "$CLUSTER_NAME-control-plane" mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/

# 2. Create manual-schedule pod
kubectl run manual-schedule --image=httpd:2-alpine

# 3. Manually schedule it
# Wait a bit for the pod to be created and pending
sleep 2
kubectl get pod manual-schedule -o json | jq '.spec.nodeName="cka-lab-26-control-plane"' | kubectl replace --force -f -

# 4. Restart scheduler
docker exec "$CLUSTER_NAME-control-plane" mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/

# 5. Create manual-schedule2 pod
# Wait for Kubelet to recreate the scheduler pod
echo "Waiting for scheduler pod to be recreated..."
until kubectl get pod -l component=kube-scheduler -n kube-system 2>/dev/null | grep -q "kube-scheduler"; do
  sleep 1
done

# Wait for scheduler to be ready
kubectl wait --for=condition=Ready pod -l component=kube-scheduler -n kube-system --timeout=60s
kubectl run manual-schedule2 --image=httpd:2-alpine

# Wait for pods to be ready
kubectl wait pod manual-schedule manual-schedule2 --for=condition=Ready --timeout=60s
