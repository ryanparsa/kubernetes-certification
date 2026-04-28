#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# tear down cluster
# N/A

rm -rf "$SCRIPT_DIR/../lab"
# Clean up potential host side artifacts from task execution
sudo rm -rf /root/oci-images
docker rmi nginx:latest 2>/dev/null || true

echo "Lab torn down."
