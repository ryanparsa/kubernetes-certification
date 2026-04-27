#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

RESULT_FILE="$SCRIPT_DIR/../lab/result.json"
mkdir -p "$(dirname "$RESULT_FILE")"

kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: api-contact
  namespace: project-swan
spec:
  serviceAccountName: secret-reader
  containers:
  - name: api-contact
    image: nginx:1-alpine
EOF

kubectl wait pod api-contact -n project-swan --for=condition=Ready --timeout=60s

kubectl exec api-contact -n project-swan -- sh -c \
  'curl -sk -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
   https://kubernetes.default/api/v1/secrets' \
  > "$RESULT_FILE"

echo "Result written to lab/result.json"
