#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Create output directory (may require elevated permissions outside the exam environment)
sudo mkdir -p /opt/course/7 && sudo chown "$(whoami)" /opt/course/7

# Wait for metrics to be available
echo "Waiting for metrics to be available..."
METRICS_READY=0
for i in $(seq 1 30); do
  if kubectl top node &>/dev/null; then
    echo "Metrics available."
    METRICS_READY=1
    break
  fi
  echo "  Attempt $i/30 - retrying in 10s..."
  sleep 10
done
if [ "$METRICS_READY" -eq 0 ]; then
  echo "Error: metrics-server did not become available after 300s"
  exit 1
fi

kubectl top pod --all-namespaces --sort-by=name --containers > /opt/course/7/pods.txt
kubectl top node --sort-by=cpu > /opt/course/7/nodes.txt

echo "Output written to /opt/course/7/pods.txt and /opt/course/7/nodes.txt"
