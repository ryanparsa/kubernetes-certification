#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"

CP_NAME="$EXAM-lab-$LAB_ID-cp"
WORKER_NAME="$EXAM-lab-$LAB_ID-worker"
export KUBECONFIG="$TASK_DIR/lab/kubeconfig.yaml"

echo "Upgrading Kubernetes packages on worker to 1.32.4..."
limactl shell "$WORKER_NAME" sudo bash -s <<'EOF'
apt-mark unhold kubeadm kubelet kubectl
apt-get install -y -q kubelet=1.32.4-* kubeadm=1.32.4-* kubectl=1.32.4-*
apt-mark hold kubelet kubeadm kubectl
systemctl daemon-reload
systemctl restart kubelet
EOF

echo "Generating join command from control plane..."
limactl shell "$CP_NAME" sudo kubeadm token create --print-join-command \
  > /tmp/cka-lab-8-join.sh

echo "Joining worker to cluster..."
limactl copy /tmp/cka-lab-8-join.sh "$WORKER_NAME:/tmp/join.sh"
limactl shell "$WORKER_NAME" sudo bash /tmp/join.sh
rm -f /tmp/cka-lab-8-join.sh

echo "Waiting for worker to become Ready..."
kubectl wait node "$WORKER_NAME" --for=condition=Ready --timeout=120s

echo ""
kubectl get nodes
