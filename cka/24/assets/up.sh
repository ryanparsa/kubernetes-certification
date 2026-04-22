#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
COURSE_DIR="$(realpath "$SCRIPT_DIR/../course")"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$COURSE_DIR"

# Generate kind config with course directory mounted at the exam-standard path
cat > /tmp/cka24-kind-config.yaml << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: cka-lab
nodes:
- role: control-plane
  extraMounts:
  - hostPath: ${COURSE_DIR}
    containerPath: /opt/course/7
EOF

kind create cluster --config /tmp/cka24-kind-config.yaml --kubeconfig "$KUBECONFIG_FILE"

echo ""
echo "Lab ready!"
echo ""
echo "To access the control plane node (needed for etcdctl snapshot):"
echo "  docker exec -it cka-lab-control-plane bash"
echo ""
echo "Inside the node, output files go to /opt/course/7/ (mapped to cka/24/course/ on your host)."
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
