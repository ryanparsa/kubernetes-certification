#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

kubectl apply -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: np-backend
  namespace: project-snake
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - to:
      - podSelector:
          matchLabels:
            app: db1
      ports:
      - protocol: TCP
        port: 1111
    - to:
      - podSelector:
          matchLabels:
            app: db2
      ports:
      - protocol: TCP
        port: 2222
EOF
