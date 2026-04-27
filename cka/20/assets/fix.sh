#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LAB_DIR="$SCRIPT_DIR/../lab"
mkdir -p "$LAB_DIR"

# Read kubelet client certificate once (outgoing connections to kube-apiserver)
CLIENT_CERT=$(docker exec cka-lab-worker \
  openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem)

CLIENT_ISSUER=$(echo "$CLIENT_CERT" | awk '/Issuer:/{gsub(/^[[:space:]]+/, ""); print; exit}')
CLIENT_EKU=$(echo "$CLIENT_CERT" | awk '/Extended Key Usage/{found=1; next} found{gsub(/^[[:space:]]+/, ""); print; exit}')

# Read kubelet server certificate once (incoming connections from kube-apiserver)
SERVER_CERT=$(docker exec cka-lab-worker \
  openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet.crt)

SERVER_ISSUER=$(echo "$SERVER_CERT" | awk '/Issuer:/{gsub(/^[[:space:]]+/, ""); print; exit}')
SERVER_EKU=$(echo "$SERVER_CERT" | awk '/Extended Key Usage/{found=1; next} found{gsub(/^[[:space:]]+/, ""); print; exit}')

# Write certificate info to file
cat > "$LAB_DIR/certificate-info.txt" <<EOF
$CLIENT_ISSUER
X509v3 Extended Key Usage: $CLIENT_EKU
$SERVER_ISSUER
X509v3 Extended Key Usage: $SERVER_EKU
EOF

echo "Certificate info written to $LAB_DIR/certificate-info.txt"
cat "$LAB_DIR/certificate-info.txt"
