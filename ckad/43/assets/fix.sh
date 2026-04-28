#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

# Ensure namespace exists
kubectl create namespace state --dry-run=client -o yaml | kubectl apply -f -

# Create PV, PVC and Pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: db-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-pvc
  namespace: state
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
---
apiVersion: v1
kind: Pod
metadata:
  name: db-pod
  namespace: state
spec:
  containers:
  - name: mysql
    image: mysql:5.7
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: rootpassword
    - name: MYSQL_DATABASE
      value: mydb
    - name: MYSQL_USER
      value: myuser
    - name: MYSQL_PASSWORD
      value: mypassword
    volumeMounts:
    - name: mysql-storage
      mountPath: /var/lib/mysql
  volumes:
  - name: mysql-storage
    persistentVolumeClaim:
      claimName: db-pvc
EOF

# Wait for pod to be ready
kubectl wait pod/db-pod -n state --for=condition=Ready --timeout=120s
