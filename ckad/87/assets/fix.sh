#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Create namespace and CronJob
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: jobs
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
  namespace: jobs
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: busybox
            command:
            - sh
            - -c
            - 'echo "Backup started at \$(date)" && sleep 5 && echo "Backup complete"'
          restartPolicy: OnFailure
EOF
