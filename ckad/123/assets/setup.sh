#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# If KUBECONFIG is not set or the file doesn't exist, and kind is available, try to get it
if [ -z "${KUBECONFIG:-}" ] && [ ! -f "$KUBECONFIG_FILE" ] && command -v kind >/dev/null 2>&1; then
  if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
    kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
  else
    kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
  fi
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Pre-seed images on the node
NODE_NAME="$CLUSTER_NAME-control-plane"

echo "Pre-seeding images on node $NODE_NAME..."
# Pulling nginx images
docker exec "$NODE_NAME" crictl pull nginx:1.20
docker exec "$NODE_NAME" crictl pull nginx:1.21

# Create an untagged image
# We pull a specific image, get its digest, remove the tag, and then pull by digest.
# This ensures an image with <none>:<none> repoTags exists.
# We use sed to filter out potential log messages (lines starting with EMMDD or level=...)
UNTAGGED_IMAGE="busybox:1.36.1"
docker exec "$NODE_NAME" crictl pull "$UNTAGGED_IMAGE"
JSON_OUTPUT=$(docker exec "$NODE_NAME" sh -c "crictl images -o json")
# Find the image ID for busybox:1.36.1 and get its repoDigest
CLEAN_JSON=$(echo "$JSON_OUTPUT" | sed '/^[EWI][0-9]\{4\}/d; /^time=/d; /^level=/d')
DIGEST=$(echo "$CLEAN_JSON" | jq -r --arg IMG "$UNTAGGED_IMAGE" '.images[] | select(.repoTags[] == $IMG) | .repoDigests[0]')
docker exec "$NODE_NAME" crictl rmi "$UNTAGGED_IMAGE"
docker exec "$NODE_NAME" crictl pull "$DIGEST"

# Create directory for the task output on the node
docker exec "$NODE_NAME" mkdir -p /opt/course/123

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready!"
