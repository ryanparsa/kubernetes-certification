#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# Wait for the node to be Ready before breaking kubelet
kubectl --kubeconfig "$KUBECONFIG_FILE" wait node --all --for=condition=Ready --timeout=120s

# Break kubelet: change service config to use wrong binary path, then stop kubelet.
# The static pod containers (API server, etcd, etc.) continue running via containerd,
# so kubectl remains accessible after kubelet stops.
docker exec cka-lab-control-plane bash -c "
  sed -i 's|ExecStart=/usr/bin/kubelet|ExecStart=/usr/local/bin/kubelet|' \
    /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
  systemctl daemon-reload
  systemctl stop kubelet
"

echo ""
echo "Lab ready! Kubelet has been intentionally broken (wrong binary path in service config)."
echo ""
echo "To access the control plane node:"
echo "  docker exec -it cka-lab-control-plane bash"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
