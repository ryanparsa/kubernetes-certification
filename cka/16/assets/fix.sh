#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

mkdir -p "$SCRIPT_DIR/../lab"

# SOLUTION

# 1. Back up the existing CoreDNS ConfigMap
kubectl -n kube-system get cm coredns -oyaml > "$SCRIPT_DIR/../lab/coredns_backup.yaml"

# 2. Add custom-domain to the kubernetes plugin line (idempotent)
COREFILE=$(kubectl -n kube-system get cm coredns -o jsonpath='{.data.Corefile}')
NEW_COREFILE=$(echo "$COREFILE" | sed 's/kubernetes cluster\.local/kubernetes custom-domain cluster.local/')
ENCODED=$(python3 -c "import sys, json; print(json.dumps(sys.argv[1]))" "$NEW_COREFILE")
kubectl -n kube-system patch cm coredns --type=merge -p "{\"data\":{\"Corefile\":$ENCODED}}"

# 3. Restart CoreDNS to pick up the new config
kubectl -n kube-system rollout restart deploy coredns
kubectl -n kube-system rollout status deploy coredns --timeout=60s
