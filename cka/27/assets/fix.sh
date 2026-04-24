#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

mkdir -p "$SCRIPT_DIR/../course"

# Step 1: Create StorageClass
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-backup
provisioner: rancher.io/local-path
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
EOF

# Step 2: Update Job manifest in course/27.yaml (Step 3 in readme)
# We need to add the PVC and update the Job to use it.
cat <<EOF > "$SCRIPT_DIR/../course/27.yaml"
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: backup-pvc
  namespace: project-bern
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Mi
  storageClassName: local-backup
---
apiVersion: batch/v1
kind: Job
metadata:
  name: backup
  namespace: project-bern
spec:
  backoffLimit: 0
  template:
    spec:
      volumes:
        - name: backup
          persistentVolumeClaim:
            claimName: backup-pvc
      containers:
        - name: bash
          image: bash:5
          command:
            - bash
            - -c
            - |
              set -x
              touch /backup/backup-\$(date +%Y-%m-%d-%H-%M-%S).tar.gz
              sleep 15
          volumeMounts:
            - name: backup
              mountPath: /backup
      restartPolicy: Never
EOF

# Step 4: Deploy and verify
kubectl apply -f "$SCRIPT_DIR/../course/27.yaml"

# Wait for Job to complete
kubectl wait --for=condition=complete job/backup -n project-bern --timeout=60s
