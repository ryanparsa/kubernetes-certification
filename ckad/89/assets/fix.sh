#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Use environment KUBECONFIG if set, otherwise use local one
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

mkdir -p "$SCRIPT_DIR/../lab"

cat <<EOF > "$SCRIPT_DIR/../lab/neb-new-job.yaml"
apiVersion: batch/v1
kind: Job
metadata:
  name: neb-new-job
  namespace: neptune
spec:
  completions: 3
  parallelism: 2
  activeDeadlineSeconds: 30
  template:
    spec:
      containers:
      - name: neb-new-job-container
        image: busybox:1.31.0
        command: ["sh", "-c", "sleep 2 && echo done"]
      restartPolicy: Never
EOF

kubectl apply -f "$SCRIPT_DIR/../lab/neb-new-job.yaml"
