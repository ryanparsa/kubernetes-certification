#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Step 1: Create namespace
kubectl create namespace minio --dry-run=client -o yaml | kubectl apply -f -

# Step 2: Install MinIO Operator via Helm
helm repo add minio https://operator.min.io
helm repo update
helm -n minio upgrade --install minio-operator minio/operator

# Step 3+4: Apply the Tenant resource with enableSFTP: true
kubectl apply -f - <<'EOF'
apiVersion: minio.min.io/v2
kind: Tenant
metadata:
  name: tenant
  namespace: minio
  labels:
    app: minio
spec:
  features:
    bucketDNS: false
    enableSFTP: true
  image: quay.io/minio/minio:latest
  pools:
  - servers: 1
    name: pool-0
    volumesPerServer: 0
    volumeClaimTemplate:
      apiVersion: v1
      kind: persistentvolumeclaims
      metadata: {}
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 10Mi
        storageClassName: standard
      status: {}
  requestAutoCert: true
EOF
