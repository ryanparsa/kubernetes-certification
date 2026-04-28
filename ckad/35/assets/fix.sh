#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
if [[ -f "$KUBECONFIG_FILE" && -z "${KUBECONFIG:-}" ]]; then
    export KUBECONFIG="$KUBECONFIG_FILE"
fi

mkdir -p "$LAB_DIR/lab"

cat <<EOF > "$LAB_DIR/lab/hello-job.yaml"
apiVersion: batch/v1
kind: Job
metadata:
  name: hello-job
  namespace: networking
spec:
  activeDeadlineSeconds: 30
  backoffLimit: 0
  template:
    spec:
      containers:
      - name: hello
        image: busybox
        command: ["sh", "-c", "echo 'Hello from Kubernetes job!'"]
      restartPolicy: Never
EOF

kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f "$LAB_DIR/lab/hello-job.yaml"

# Wait for job to complete (it should be very fast)
kubectl wait --for=condition=complete job/hello-job -n networking --timeout=60s
