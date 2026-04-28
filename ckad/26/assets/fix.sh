#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: workloads
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: log-cleaner
  namespace: workloads
spec:
  schedule: "0 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: log-cleaner
            image: busybox
            command: ["/bin/sh", "-c"]
            args:
            - find /var/log -type f -name "*.log" -mtime +7 -delete
          restartPolicy: OnFailure
EOF
