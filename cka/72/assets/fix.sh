#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine KUBECONFIG
if [[ -z "${KUBECONFIG:-}" ]]; then
  if [[ -f "$SCRIPT_DIR/kubeconfig.yaml" ]]; then
    export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
  elif [[ -f "$HOME/.kube/config" ]]; then
    export KUBECONFIG="$HOME/.kube/config"
  fi
fi

COURSE_DIR="$SCRIPT_DIR/../course"
mkdir -p "$COURSE_DIR"

# 1) Write all context names
kubectl config get-contexts -o name > "$COURSE_DIR/contexts"

# 2) Write command to display current context using kubectl
echo "kubectl config current-context" > "$COURSE_DIR/context_default_kubectl"

# 3) Write command to display current context without kubectl
# In a real exam, this would probably be ~/.kube/config
# For this lab, we point to whatever KUBECONFIG is currently active.
KCONFIG_PATH="${KUBECONFIG:-$HOME/.kube/config}"
echo "grep 'current-context' $KCONFIG_PATH | awk '{print \$2}'" > "$COURSE_DIR/context_default_sh"
