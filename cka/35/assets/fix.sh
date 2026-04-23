#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SCRIPT_DIR/../course"

cat > "$SCRIPT_DIR/../course/etcd-info.txt" <<EOT
Server private key location: /etc/kubernetes/pki/etcd/server.key
Server certificate expiration date: Oct 29 14:19:29 2025 GMT
Is client certificate authentication enabled: yes
EOT
