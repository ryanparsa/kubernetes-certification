#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
fi

RESULT_FILE="$SCRIPT_DIR/../course/26/result.json"
mkdir -p "$(dirname "$RESULT_FILE")"

# Ensure pre-requisites are applied (especially for CI where up.sh might be skipped)
kubectl apply -f "$SCRIPT_DIR/workloads.yaml"

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

echo "Result written to course/26/result.json"
