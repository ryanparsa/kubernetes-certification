#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# 1. Stop scheduler
docker exec "$CLUSTER_NAME-control-plane" mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/

# Wait for scheduler pod to be gone
until ! kubectl get pod -n kube-system -l component=kube-scheduler 2>/dev/null | grep -q "kube-scheduler"; do
  sleep 2
done

# 2. Create pod
kubectl run manual-schedule --image=httpd:2-alpine

# 3. Manually schedule
kubectl get pod manual-schedule -o json | jq '.spec.nodeName="cka-lab-9-control-plane"' | kubectl replace --force -f -

kubectl wait pod manual-schedule --for=condition=Ready --timeout=60s

# 4. Start scheduler again
docker exec "$CLUSTER_NAME-control-plane" mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/

# Wait for scheduler pod to be back
until kubectl get pod -n kube-system -l component=kube-scheduler 2>/dev/null | grep -q "Running"; do
  sleep 2
done

# 5. Create second pod
kubectl run manual-schedule2 --image=httpd:2-alpine

kubectl wait pod manual-schedule2 --for=condition=Ready --timeout=60s
