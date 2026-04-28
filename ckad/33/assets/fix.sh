#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: public-web
  namespace: networking
spec:
  type: NodePort
  selector:
    app: web-frontend
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080
EOF

kubectl wait service public-web -n networking --for=jsonpath='{.spec.type}'=NodePort --timeout=30s
