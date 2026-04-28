#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# 1. Stop scheduler
docker exec cka-lab-108-control-plane mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/

# 2. Create manual-schedule pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: manual-schedule
spec:
  containers:
  - name: httpd
    image: httpd:2.4-alpine
EOF

# 3. Manually schedule
kubectl get pod manual-schedule -o json | jq '.spec.nodeName="cka-lab-108-worker"' | kubectl replace --force -f -
kubectl wait pod manual-schedule --for=condition=Ready --timeout=60s

# 4. Start scheduler
docker exec cka-lab-108-control-plane mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/

# 5. Create manual-schedule2
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: manual-schedule2
spec:
  containers:
  - name: httpd
    image: httpd:2.4-alpine
EOF

kubectl wait pod manual-schedule2 --for=condition=Ready --timeout=60s
