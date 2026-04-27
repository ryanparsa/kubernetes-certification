#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"

CP_NAME="$EXAM-lab-$LAB_ID-cp"
WORKER_NAME="$EXAM-lab-$LAB_ID-worker"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

command -v limactl &>/dev/null || { echo "Error: 'limactl' not found. Install Lima: https://lima-vm.io"; exit 1; }

mkdir -p "$TASK_DIR/lab"

echo "Starting control plane VM ($CP_NAME)..."
limactl start --name "$CP_NAME" "$SCRIPT_DIR/control-plane.yaml"

echo "Provisioning control plane..."
limactl copy "$SCRIPT_DIR/provision-control-plane.sh" "$CP_NAME:/tmp/provision.sh"
limactl shell "$CP_NAME" sudo bash /tmp/provision.sh

echo "Starting worker VM ($WORKER_NAME)..."
limactl start --name "$WORKER_NAME" "$SCRIPT_DIR/worker.yaml"

echo "Provisioning worker..."
limactl copy "$SCRIPT_DIR/provision-worker.sh" "$WORKER_NAME:/tmp/provision.sh"
limactl shell "$WORKER_NAME" sudo bash /tmp/provision.sh

echo "Copying kubeconfig..."
limactl copy "$CP_NAME:/etc/kubernetes/admin.conf" "$KUBECONFIG_FILE"

CP_IP=$(limactl shell "$CP_NAME" hostname -I | awk '{print $1}')
sed -i.bak "s|server: https://.*:6443|server: https://$CP_IP:6443|" "$KUBECONFIG_FILE"
rm -f "${KUBECONFIG_FILE}.bak"

echo ""
echo "Lab ready!"
echo ""
printf "  %-16s %s  Kubernetes 1.32.4\n" "Control plane:" "$CP_NAME"
printf "  %-16s %s  Kubernetes 1.31.8 (not joined)\n" "Worker:" "$WORKER_NAME"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=lab/kubeconfig.yaml"
echo ""
echo "SSH into nodes:"
echo "  limactl shell $CP_NAME"
echo "  limactl shell $WORKER_NAME"
