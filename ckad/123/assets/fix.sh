#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
NODE_NAME="$CLUSTER_NAME-control-plane"

# We use docker exec to run crictl on the node because crictl is only available inside the kind node
docker exec "$NODE_NAME" sh -c "crictl images > /opt/course/123/images"

# Function to run crictl and return clean JSON
crictl_json() {
  docker exec "$NODE_NAME" sh -c "crictl images -o json" | sed '/^[EWI][0-9]\{4\}/d; /^time=/d; /^level=/d'
}

NGINX_IDS=$(crictl_json | jq -r '.images[] | select(.repoTags[] | contains("nginx")) | .id')
for ID in $NGINX_IDS; do
  docker exec "$NODE_NAME" crictl rmi "$ID" || true
done

UNTAGGED_IDS=$(crictl_json | jq -r '.images[] | select(.repoTags | length == 0 or .repoTags[0] == "<none>:<none>") | .id')
for ID in $UNTAGGED_IDS; do
  docker exec "$NODE_NAME" crictl rmi "$ID" || true
done
