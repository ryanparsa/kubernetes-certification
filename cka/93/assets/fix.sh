#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
CONTAINER="${CLUSTER_NAME}-control-plane"

# 1. Extract the apiserver certificate expiration date, reformat to mm/dd/YYYY
EXPIRY_RAW=$(docker exec "$CONTAINER" openssl x509 -noout -enddate \
  -in /etc/kubernetes/pki/apiserver.crt | cut -d= -f2)

# date -d parses the openssl format: "Apr 27 06:12:47 2026 GMT"
EXPIRY_FMT=$(date -d "$EXPIRY_RAW" "+%m/%d/%Y")

# 2. Write files into the container
docker exec "$CONTAINER" mkdir -p /opt/course/14
docker exec "$CONTAINER" bash -c "echo '${EXPIRY_FMT}' > /opt/course/14/expiration"
docker exec "$CONTAINER" bash -c "echo 'kubeadm certs renew apiserver' > /opt/course/14/kubeadm-renew-certs.txt"

echo "Expiration written (${EXPIRY_FMT}) -> /opt/course/14/expiration"
echo "Renewal command written -> /opt/course/14/kubeadm-renew-certs.txt"
