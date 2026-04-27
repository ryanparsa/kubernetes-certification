#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

LAB_DIR="$SCRIPT_DIR/../lab"
mkdir -p "$LAB_DIR"

# 1. Make a backup of the existing configuration YAML
kubectl -n kube-system get cm coredns -o yaml > "$LAB_DIR/coredns_backup.yaml"

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
lines = corefile.splitlines(keepends=True)
updated = False

for i, line in enumerate(lines):
    stripped = line.lstrip()
    if not stripped.startswith("kubernetes "):
        continue
    if "custom-domain" in stripped:
        continue
    if "cluster.local" not in stripped:
        continue
    lines[i] = line.replace("cluster.local", "custom-domain cluster.local", 1)
    updated = True
    break

if updated:
    cm["data"]["Corefile"] = "".join(lines)

# Apply updated config
cmd = ["kubectl", "apply", "-f", "-"]
kconfig = os.environ.get("KUBECONFIG")
if kconfig and os.path.exists(kconfig):
    cmd.insert(1, "--kubeconfig")
    cmd.insert(2, kconfig)

result = subprocess.run(
    cmd,
    input=json.dumps(cm),
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    if result.stderr:
        sys.stderr.write(result.stderr)
    sys.exit(result.returncode)
EOF

# Restart CoreDNS deployment to pick up changes
kubectl -n kube-system rollout restart deploy coredns
kubectl -n kube-system rollout status deploy coredns --timeout=60s
