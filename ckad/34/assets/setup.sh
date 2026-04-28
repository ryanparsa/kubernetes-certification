#!/usr/bin/env bash
set -euo pipefail

# 1. Check dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

if ! command -v kind &> /dev/null; then
    echo "kind is not installed. Please install it first."
    exit 1
fi

# 2. Create cluster
if ! kind get clusters | grep -q "$CLUSTER_NAME"; then
    kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

if [[ -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

# 3. Apply pre-existing workloads
kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
kubectl create service clusterip api-service -n networking --tcp=80:80 --dry-run=client -o yaml | kubectl apply -f -

# 4. Wait for deployments
# N/A

# 5. Create the output directory
mkdir -p "$SCRIPT_DIR/../lab"

# 6. Copy task assets
# N/A

# 7. Print summary
echo "Lab ready!"
echo "Run the following command to use the lab's kubeconfig:"
echo "export KUBECONFIG=$KUBECONFIG_FILE"
