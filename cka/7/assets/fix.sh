#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$SCRIPT_DIR/../course"

mkdir -p "$COURSE_DIR"

cat > "$COURSE_DIR/node.sh" <<'EOF'
kubectl top node
EOF

cat > "$COURSE_DIR/pod.sh" <<'EOF'
kubectl top pod --containers=true
EOF

echo "Scripts written to course/node.sh and course/pod.sh"
