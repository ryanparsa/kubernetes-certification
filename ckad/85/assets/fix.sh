#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

mkdir -p "$SCRIPT_DIR/../lab"

# Create namespace (idempotent)
kubectl create namespace secure --dry-run=client -o yaml | kubectl apply -f -

# Create ConfigMap (idempotent)
kubectl create configmap app-config \
  --from-literal=key=value \
  -n secure \
  --dry-run=client -o yaml | kubectl apply -f -

# Write Pod manifest
cat <<EOF > "$SCRIPT_DIR/../lab/secure-app.yaml"
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: secure
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: alpine
    command: ["sleep", "3600"]
    securityContext:
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
    volumeMounts:
    - name: config-vol
      mountPath: /config
  volumes:
  - name: config-vol
    configMap:
      name: app-config
EOF

kubectl apply -f "$SCRIPT_DIR/../lab/secure-app.yaml"
kubectl wait pod/secure-app -n secure --for=condition=Ready --timeout=60s
