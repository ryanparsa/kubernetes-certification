#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$SCRIPT_DIR/../lab"

mkdir -p "$LAB_DIR"

cat > "$LAB_DIR/find_pods.sh" <<'EOF'
kubectl get pod -A --sort-by=.metadata.creationTimestamp
EOF

cat > "$LAB_DIR/find_pods_uid.sh" <<'EOF'
kubectl get pod -A --sort-by=.metadata.uid
EOF

chmod +x "$LAB_DIR/find_pods.sh" "$LAB_DIR/find_pods_uid.sh"

echo "Solution applied."
