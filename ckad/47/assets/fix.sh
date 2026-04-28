#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

cat <<EOF > "$SCRIPT_DIR/../lab/47.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: security
---
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: security
spec:
  securityContext:
    runAsUser: 1000
    runAsNonRoot: true
  containers:
  - name: nginx
    image: nginx:alpine
    command: ["sleep", "3600"]
    securityContext:
      capabilities:
        drop: ["ALL"]
      readOnlyRootFilesystem: true
      runAsNonRoot: true
EOF

kubectl apply -f "$SCRIPT_DIR/../lab/47.yaml"
kubectl wait pod/secure-app -n security --for=condition=Ready --timeout=60s
