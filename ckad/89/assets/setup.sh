#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# Create cluster if it doesn't exist
if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# Pre-seed images on the node
NODE_NAME="$CLUSTER_NAME-control-plane"

echo "Pre-seeding images on node $NODE_NAME..."
# Pulling nginx images
docker exec "$NODE_NAME" crictl pull nginx:1.20
docker exec "$NODE_NAME" crictl pull nginx:1.21

# Pull an image by digest to ensure it shows up as <none>:<none>
# Using a specific digest for alpine to be safe
ALPINE_DIGEST="alpine@sha256:21a3007f35907953047f3109315570081d48c8b6727282b936a29d5a7698a96e"
docker exec "$NODE_NAME" crictl pull "$ALPINE_DIGEST"

# Create directory for the task output on the node
docker exec "$NODE_NAME" mkdir -p /opt/course/4

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
