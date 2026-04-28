#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$SCRIPT_DIR/../lab"
MANIFEST="$LAB_DIR/44.yaml"

mkdir -p "$LAB_DIR"

cat <<'EOF' > "$MANIFEST"
apiVersion: v1
kind: Namespace
metadata:
  name: pod-design
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
  namespace: pod-design
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      activeDeadlineSeconds: 100
      template:
        spec:
          containers:
          - name: backup
            image: busybox
            command: ['sh', '-c', 'echo Backup started: $(date); sleep 30; echo Backup completed: $(date)']
          restartPolicy: OnFailure
EOF

kubectl apply -f "$MANIFEST"
