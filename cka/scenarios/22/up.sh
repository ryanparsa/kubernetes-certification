#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-22 --kubeconfig "$KUBECONFIG"

# Create a private key and CSR for a user "john"
openssl genrsa -out "$DIR/john.key" 2048
openssl req -new -key "$DIR/john.key" -out "$DIR/john.csr" -subj "/CN=john"
CSR_BASE64=$(cat "$DIR/john.csr" | base64 | tr -d '\n')

# Create the CSR object in K8s
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  request: $CSR_BASE64
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
  - client auth
EOF

echo "CSR 'john-developer' created in Pending state."
