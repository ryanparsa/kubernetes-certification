#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$SCRIPT_DIR/../lab"

mkdir -p "$LAB_DIR"

cat > "$LAB_DIR/node.sh" <<'EOF'
kubectl top node
EOF

cat > "$LAB_DIR/pod.sh" <<'EOF'
kubectl top pod --containers=true
EOF

echo "Scripts written to lab/node.sh and lab/pod.sh"
