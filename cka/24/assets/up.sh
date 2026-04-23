#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker curl python3; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create the course/ output directory (needed before cluster for extraMounts)
mkdir -p "$SCRIPT_DIR/../course"

# 3. Create cluster
# Move to script directory so relative paths in kind-config.yaml resolve correctly
cd "$SCRIPT_DIR"
kind create cluster --name "$CLUSTER_NAME" --config "kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 4. Wait for deployments
echo "Waiting for etcd to be ready..."
kubectl wait --kubeconfig "$KUBECONFIG_FILE" -n kube-system --for=condition=Ready pod -l component=etcd --timeout=120s

# 5. Install etcdctl/etcdutl on the control-plane node
echo "Installing etcdctl and etcdutl on the control-plane node..."
ETCD_VERSION="v3.5.16"
DOWNLOAD_URL="https://github.com/etcd-io/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz"

docker exec "$CLUSTER_NAME-control-plane" sh -c "
  curl -L ${DOWNLOAD_URL} -o /tmp/etcd.tar.gz && \
  tar xzvf /tmp/etcd.tar.gz -C /tmp && \
  mv /tmp/etcd-${ETCD_VERSION}-linux-amd64/etcdctl /usr/local/bin/ && \
  mv /tmp/etcd-${ETCD_VERSION}-linux-amd64/etcdutl /usr/local/bin/ && \
  rm -rf /tmp/etcd*
"

# 6. Apply pre-existing workloads (N/A)

# 7. Print summary
echo ""
echo "Lab ready!"
echo ""
echo "To access the control plane node (needed for etcdctl snapshot):"
echo "  docker exec -it $CLUSTER_NAME-control-plane bash"
echo ""
echo "Inside the node, output files go to /opt/course/$LAB_ID/ (mapped to $EXAM/$LAB_ID/course/ on your host)."
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
