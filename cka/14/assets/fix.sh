#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# Extract the apiserver certificate expiration date from inside the container
# We use the same format as seen in the readme.md answer section: Oct 29 14:19:27 2025 GMT
# openssl x509 -enddate -noout -in ... returns "notAfter=Oct 29 14:19:27 2025 GMT"
EXPIRY=$(docker exec "${CLUSTER_NAME}-control-plane" openssl x509 -noout -enddate \
  -in /etc/kubernetes/pki/apiserver.crt | cut -d= -f2)

mkdir -p "$SCRIPT_DIR/../course"

echo "$EXPIRY" > "$SCRIPT_DIR/../course/expiration"
echo "kubeadm certs renew apiserver" > "$SCRIPT_DIR/../course/kubeadm-renew-certs.sh"

echo "Expiration written: $EXPIRY"
echo "Renewal script written."
