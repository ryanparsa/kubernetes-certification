#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# Provision cluster
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
export KUBECONFIG="$KUBECONFIG_FILE"

mkdir -p "$SCRIPT_DIR/../lab"

# Create the directory where the output should be saved
# Since this is a kind lab, the "host" is the machine running kind.
# However, many lab questions assume they are running on a jumpbox or control-plane where /opt/course/ exists.
# Based on cka/95/assets/fix.sh, it seems they use docker exec to create it on the control-plane.
# But ckad/89/README.md just says /opt/course/1/namespaces.
# If I'm a student running kubectl on my laptop, /opt/course/1/ would be on my laptop.
# If the check script runs on my laptop, it will look for /opt/course/1/namespaces on my laptop.

# I'll create it locally and handle potential permission issues.
sudo mkdir -p /opt/course/1
sudo chmod 777 /opt/course/1

echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
