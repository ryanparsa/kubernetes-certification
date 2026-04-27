#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

# Ensure lab directory exists
mkdir -p "$SCRIPT_DIR/../lab"

# Create Namespace
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: secret
EOF

# Create Secret 1 from file, injecting namespace
# Note: In CI, we need to make sure the file exists.
# Since we are not running setup.sh, we use the source of truth if lab file is missing.
SOURCE_SECRET="$SCRIPT_DIR/../lab/28_secret1.yaml"
if [ ! -f "$SOURCE_SECRET" ]; then
    SOURCE_SECRET="$SCRIPT_DIR/task-secret1.yaml"
fi
sed 's/metadata:/metadata:\n  namespace: secret/' "$SOURCE_SECRET" | kubectl apply -f -

# Create Secret 2
kubectl -n secret create secret generic secret2 \
  --from-literal=user=user1 \
  --from-literal=pass=1234 \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: secret-pod
  name: secret-pod
  namespace: secret
spec:
  containers:
  - args:
    - sh
    - -c
    - sleep 1d
    image: busybox:1
    name: secret-pod
    env:
    - name: APP_USER
      valueFrom:
        secretKeyRef:
          name: secret2
          key: user
    - name: APP_PASS
      valueFrom:
        secretKeyRef:
          name: secret2
          key: pass
    volumeMounts:
    - name: secret1
      mountPath: /tmp/secret1
      readOnly: true
  volumes:
  - name: secret1
    secret:
      secretName: secret1
EOF

kubectl wait pod secret-pod -n secret --for=condition=Ready --timeout=60s
