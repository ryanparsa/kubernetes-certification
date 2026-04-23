#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
CLUSTER_NAME="cka-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Create the course/ output directory for writing expiration and renewal script
mkdir -p "$SCRIPT_DIR/../course"

echo ""
echo "Lab ready!"
echo ""
echo "The kube-apiserver certificate is inside the control-plane container."
echo "To access it, exec into the container:"
echo "  docker exec -it ${CLUSTER_NAME}-control-plane bash"
echo ""
echo "Inside the container you can run:"
echo "  openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep Validity -A2"
echo "  kubeadm certs check-expiration | grep apiserver"
echo ""
echo "Write the expiration date to: cka/14/course/expiration"
echo "Write the renewal command to: cka/14/course/kubeadm-renew-certs.sh"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
