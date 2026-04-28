#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/../lab/kubeconfig.yaml}"

# 1. Create namespace
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: networking
EOF

# 2. Create pods
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: secure-db
  namespace: networking
  labels:
    app: db
spec:
  containers:
  - name: postgres
    image: postgres:12
    env:
    - name: POSTGRES_PASSWORD
      value: password
---
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: networking
  labels:
    role: frontend
spec:
  containers:
  - name: nginx
    image: nginx
---
apiVersion: v1
kind: Pod
metadata:
  name: monitoring
  namespace: networking
  labels:
    role: monitoring
spec:
  containers:
  - name: nginx
    image: nginx
EOF

# 3. Create NetworkPolicy
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-network-policy
  namespace: networking
spec:
  podSelector:
    matchLabels:
      app: db
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
      port: 5432
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: monitoring
    ports:
    - protocol: TCP
      port: 8080
EOF

# 4. Wait for pods to be ready
kubectl wait --for=condition=Ready pod/secure-db pod/frontend pod/monitoring -n networking --timeout=60s
