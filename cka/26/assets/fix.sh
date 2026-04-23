#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Stop the scheduler
docker exec cka-lab-26-control-plane mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/

# Wait for scheduler pod to be gone
until ! kubectl -n kube-system get pod -l component=kube-scheduler -o name | grep -q .; do
  sleep 2
done

# 2. Create manual-schedule pod
kubectl run manual-schedule --image=httpd:2-alpine

# 3. Manually schedule it
# Wait a bit to ensure it's Pending
sleep 2

# Manually schedule by setting nodeName and replacing the pod
kubectl get pod manual-schedule -o json | jq '.spec.nodeName="cka-lab-26-control-plane"' | kubectl replace --force -f -

# 4. Restart the scheduler
docker exec cka-lab-26-control-plane mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/

# Wait for scheduler to be Running
kubectl -n kube-system wait pod -l component=kube-scheduler --for=condition=Ready --timeout=60s

# 5. Create manual-schedule2 pod
kubectl run manual-schedule2 --image=httpd:2-alpine

# Wait for pods to be Ready
kubectl wait pod manual-schedule manual-schedule2 --for=condition=Ready --timeout=60s
