#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Wait for node readiness
kubectl --kubeconfig "$KUBECONFIG_FILE" wait node --all --for=condition=Ready --timeout=120s

# 4. Break the kubelet
# The static pod containers (API server, etcd, etc.) continue running via containerd,
# so kubectl remains accessible after kubelet stops.
docker exec cka-lab-control-plane bash -c "
  sed -i 's|ExecStart=/usr/bin/kubelet|ExecStart=/usr/local/bin/kubelet|' \
    /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
  systemctl daemon-reload
  systemctl stop kubelet
"

# 5. Print summary
echo ""
echo "Lab ready! Kubelet has been intentionally broken (wrong binary path in service config)."
echo ""
echo "To access the control plane node:"
echo "  docker exec -it cka-lab-control-plane bash"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
