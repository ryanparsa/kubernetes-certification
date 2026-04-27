#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

CONTROL_PLANE_NODE="$CLUSTER_NAME-control-plane"
ETCD_MANIFEST="/etc/kubernetes/manifests/etcd.yaml"

# Extract information from the cluster
KEY_FILE=$(docker exec "$CONTROL_PLANE_NODE" grep "\-\-key-file=" "$ETCD_MANIFEST" | cut -d= -f2)
CLIENT_AUTH=$(docker exec "$CONTROL_PLANE_NODE" grep "\-\-client-cert-auth=" "$ETCD_MANIFEST" | cut -d= -f2)
CERT_FILE=$(docker exec "$CONTROL_PLANE_NODE" grep "\-\-cert-file=" "$ETCD_MANIFEST" | cut -d= -f2)

# Get expiration date from certificate
EXPIRY=$(docker exec "$CONTROL_PLANE_NODE" openssl x509 -noout -enddate -in "$CERT_FILE" | cut -d= -f2)

# Map true/false to yes/no
CLIENT_AUTH_YES_NO="no"
if [ "$CLIENT_AUTH" == "true" ]; then
    CLIENT_AUTH_YES_NO="yes"
fi

# Write to the lab file
mkdir -p "$SCRIPT_DIR/../lab"
cat <<EOF > "$SCRIPT_DIR/../lab/etcd-info.txt"
Server private key location: $KEY_FILE
Server certificate expiration date: $EXPIRY
Is client certificate authentication enabled: $CLIENT_AUTH_YES_NO
EOF
