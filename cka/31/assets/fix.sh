#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SCRIPT_DIR/../course"

cat <<EOF > "$SCRIPT_DIR/../course/cluster-info"
1: 1
2: 0
3: 10.96.0.0/12
4: kindnet, /etc/cni/net.d/10-kindnet.conflist
5: -cka-lab-31-control-plane
EOF
