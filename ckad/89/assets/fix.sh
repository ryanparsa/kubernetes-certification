#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${GITHUB_ACTIONS:-}" ]]; then
    KUBECONFIG_FILE="${HOME}/.kube/config"
else
    KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
fi
export KUBECONFIG="$KUBECONFIG_FILE"

# Create the Pod
kubectl run pod1 --image=httpd:2.4.41-alpine --port=80

# Wait for Pod to be ready
kubectl wait pod pod1 --for=condition=Ready --timeout=60s

# Expose as NodePort Service
kubectl expose pod pod1 --name=pod1-svc --type=NodePort --port=80

# Write the command to file
# On a real cluster, this would be /opt/course/89/pod1-svc.sh on the node.
# Here we simulate it by writing to the hostPath mount.
mkdir -p "$SCRIPT_DIR/course"
echo "kubectl expose pod pod1 --name=pod1-svc --type=NodePort --port=80" > "$SCRIPT_DIR/course/pod1-svc.sh"
chmod +x "$SCRIPT_DIR/course/pod1-svc.sh"
