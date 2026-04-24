#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

COURSE_DIR="$SCRIPT_DIR/../course"
mkdir -p "$COURSE_DIR"

# 1. Make a backup of the existing configuration YAML
kubectl -n kube-system get cm coredns -o yaml > "$COURSE_DIR/coredns_backup.yaml"

# 2. Update the CoreDNS configuration
# We use a python script to safely modify the ConfigMap data
python3 - <<EOF
import sys
import json
import subprocess
import os

def kubectl(*args):
    cmd = ["kubectl"]
    kconfig = os.environ.get("KUBECONFIG")
    if kconfig and os.path.exists(kconfig):
        cmd.extend(["--kubeconfig", kconfig])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# Get current config
cm_json = kubectl("-n", "kube-system", "get", "cm", "coredns", "-o", "json")
cm = json.loads(cm_json)

# Modify Corefile
corefile = cm["data"]["Corefile"]
if "custom-domain" not in corefile:
    corefile = corefile.replace("cluster.local", "custom-domain cluster.local")
    cm["data"]["Corefile"] = corefile

# Apply updated config
cmd = ["kubectl", "apply", "-f", "-"]
kconfig = os.environ.get("KUBECONFIG")
if kconfig and os.path.exists(kconfig):
    cmd.insert(1, "--kubeconfig")
    cmd.insert(2, kconfig)

process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
process.communicate(json.dumps(cm))
EOF

# Restart CoreDNS deployment to pick up changes
kubectl -n kube-system rollout restart deploy coredns
kubectl -n kube-system rollout status deploy coredns --timeout=60s
