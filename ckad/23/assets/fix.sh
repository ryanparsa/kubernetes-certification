#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Ensure namespace exists
kubectl create namespace troubleshooting --dry-run=client -o yaml | kubectl apply -f -

# Wait for default service account to be provisioned
until kubectl get serviceaccount default -n troubleshooting --no-headers 2>/dev/null | grep -q default; do
  sleep 1
done

# Delete existing pod (if any) so we can re-create with resource limits applied
kubectl delete pod logging-pod -n troubleshooting --ignore-not-found

# Re-create the pod with CPU and memory limits on the log-processor container
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: logging-pod
  namespace: troubleshooting
spec:
  containers:
  - name: log-collector
    image: nginx:alpine
  - name: log-processor
    image: busybox:1.36
    command: ["sh", "-c", "while true; do echo processing; sleep 1; done"]
    resources:
      limits:
        cpu: 100m
        memory: 50Mi
EOF

kubectl wait pod logging-pod -n troubleshooting --for=condition=Ready --timeout=60s
