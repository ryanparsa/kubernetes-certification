#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create namespace
kubectl create ns secret --dry-run=client -o yaml | kubectl apply -f -

# 2. Create secret1 from course/secret1.yaml
# We ensure the namespace is set to 'secret' using a temporary manifest
kubectl get secret -n default secret1 --dry-run=client -o yaml || true # This might not work if it's not applied yet
# Actually we can just apply it with the namespace flag if it doesn't have one,
# but the task says to "create the existing secret cka/28/course/secret1.yaml".
# In fix.sh we should simulate the correct final state.

kubectl apply -f - <<EOF
$(cat "$SCRIPT_DIR/../course/secret1.yaml")
EOF
# The above might fail if it has no namespace or wrong namespace.
# Let's use sed to add/replace namespace if needed, or just pipe to kubectl with -n
cat "$SCRIPT_DIR/../course/secret1.yaml" | sed '/metadata:/a \  namespace: secret' | kubectl apply -f -

# 3. Create secret2
kubectl -n secret create secret generic secret2 \
  --from-literal=user=user1 \
  --from-literal=pass=1234 \
  --dry-run=client -o yaml | kubectl apply -f -

# 4. Create Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
  namespace: secret
  labels:
    run: secret-pod
spec:
  containers:
  - name: secret-pod
    image: busybox:1
    args:
    - sh
    - -c
    - sleep 1d
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
