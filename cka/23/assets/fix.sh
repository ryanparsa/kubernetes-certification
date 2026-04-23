#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Fix the kubelet binary path in the service config
docker exec "$CLUSTER_NAME-control-plane" bash -c "
  sed -i 's|ExecStart=/usr/local/bin/kubelet|ExecStart=/usr/bin/kubelet|' \
    /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
  systemctl daemon-reload
  systemctl restart kubelet
"

# 2. Wait for the node to be Ready
kubectl wait node "$CLUSTER_NAME-control-plane" --for=condition=Ready --timeout=120s

# 3. Create the Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: success
  namespace: default
spec:
  containers:
  - name: success
    image: nginx:1-alpine
EOF

kubectl wait pod success -n default --for=condition=Ready --timeout=60s
