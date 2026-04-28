#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Create namespace
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -

# Create Secret
kubectl create secret generic db-credentials -n workloads \
  --from-literal=username=admin \
  --from-literal=password=securepass \
  --from-literal=random=true \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
  namespace: workloads
spec:
  containers:
  - name: mysql
    image: mysql:9.5.0
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
    - name: MYSQL_RANDOM_ROOT_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: random
  restartPolicy: Always
EOF

kubectl wait pod secure-pod -n workloads --for=condition=Ready --timeout=120s
