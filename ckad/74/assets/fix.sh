#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOCAL_KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$LOCAL_KUBECONFIG" ]; then
  export KUBECONFIG="$LOCAL_KUBECONFIG"
fi

kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: secured
  name: secured
spec:
  securityContext:
    fsGroup: 3000
  containers:
  - image: nginx
    name: secured
    volumeMounts:
    - name: data-vol
      mountPath: /data/app
    resources: {}
  volumes:
  - name: data-vol
    emptyDir: {}
  dnsPolicy: ClusterFirst
EOF

kubectl wait pod/secured --for=condition=Ready --timeout=60s

# Create a file in the volume to verify fsGroup ownership
kubectl exec secured -- sh -c 'touch /data/app/logs.txt'
