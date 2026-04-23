#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$SCRIPT_DIR/../course"

mkdir -p "$COURSE_DIR"

cat > "$COURSE_DIR/find_pods.sh" <<'EOF'
kubectl get pod -A --sort-by=.metadata.creationTimestamp
EOF

cat > "$COURSE_DIR/find_pods_uid.sh" <<'EOF'
kubectl get pod -A --sort-by=.metadata.uid
EOF

chmod +x "$COURSE_DIR/find_pods.sh" "$COURSE_DIR/find_pods_uid.sh"

echo "Solution applied."
