#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: network-test
---
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: network-test
  labels:
    role: frontend
spec:
  containers:
  - name: frontend
    image: nginx
---
apiVersion: v1
kind: Pod
metadata:
  name: api
  namespace: network-test
  labels:
    role: api
spec:
  containers:
  - name: api
    image: nginx
---
apiVersion: v1
kind: Pod
metadata:
  name: db
  namespace: network-test
  labels:
    role: db
spec:
  containers:
  - name: db
    image: nginx
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: network-test
spec:
  podSelector:
    matchLabels:
      role: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: db
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
EOF

kubectl wait pod frontend -n network-test --for=condition=Ready --timeout=60s
kubectl wait pod api -n network-test --for=condition=Ready --timeout=60s
kubectl wait pod db -n network-test --for=condition=Ready --timeout=60s
