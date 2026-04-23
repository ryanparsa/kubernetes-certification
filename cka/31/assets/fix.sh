#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$SCRIPT_DIR/../course"

mkdir -p "$COURSE_DIR"

cat > "$COURSE_DIR/cluster-info" <<EOF
# cka/31/course/cluster-info

# How many controlplane *Nodes* are available?
1: 1

# How many worker *Nodes* (non controlplane *Nodes*) are available?
2: 0

# What is the *Service* CIDR?
3: 10.96.0.0/12

# Which Networking (or CNI Plugin) is configured and where is its config file?
4: kindnet, /etc/cni/net.d/10-kindnet.conflist

# Which suffix will static *Pods* have that run on cka-lab-31-control-plane?
5: -cka-lab-31-control-plane
EOF
