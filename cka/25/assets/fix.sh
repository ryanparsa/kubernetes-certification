#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$SCRIPT_DIR/../course"

mkdir -p "$COURSE_DIR"

cat > "$COURSE_DIR/controlplane-components.txt" <<EOF
kubelet: process
kube-apiserver: static-pod
kube-scheduler: static-pod
kube-controller-manager: static-pod
etcd: static-pod
dns: pod coredns
EOF
