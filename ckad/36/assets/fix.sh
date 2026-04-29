#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Pull the nginx:latest image
docker pull nginx:latest

# 2. Create the directory
sudo mkdir -p /root/oci-images

# 3. Export the nginx image in OCI format
docker save nginx:latest -o /tmp/nginx-image.tar
sudo tar -xf /tmp/nginx-image.tar -C /root/oci-images
rm -f /tmp/nginx-image.tar
