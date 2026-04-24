#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Stop the kube-scheduler
docker exec "${CLUSTER_NAME}-control-plane" mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/
# Wait for it to disappear
while kubectl get pod -n kube-system -l component=kube-scheduler 2>/dev/null | grep -q kube-scheduler; do sleep 1; done

# 2. Create manual-schedule pod
kubectl run manual-schedule --image=httpd:2-alpine

# 3. Manually schedule the pod
kubectl get pod manual-schedule -o json | jq ".spec.nodeName=\"${CLUSTER_NAME}-control-plane\"" | kubectl replace --force -f -

# 4. Restart the kube-scheduler
docker exec "${CLUSTER_NAME}-control-plane" mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/
# Wait for it to be running again
until kubectl get pod -n kube-system -l component=kube-scheduler 2>/dev/null | grep -q Running; do sleep 1; done

# 5. Create manual-schedule2 pod
kubectl run manual-schedule2 --image=httpd:2-alpine

# Wait for both pods to be ready
kubectl wait pod manual-schedule manual-schedule2 --for=condition=Ready --timeout=60s
