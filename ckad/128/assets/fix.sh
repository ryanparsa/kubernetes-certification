#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

mkdir -p "$SCRIPT_DIR/../lab"

# Get existing deployment and modify it
# In a real scenario, the student would do this.
# Here we just apply the desired state.

cat <<EOF > "$SCRIPT_DIR/../lab/pluto-deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pluto-deployment
  namespace: pluto
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pluto-app
  template:
    metadata:
      labels:
        app: pluto-app
    spec:
      containers:
      - name: pluto-app
        image: nginx:1.25.3
        volumeMounts:
        - name: log-data
          mountPath: /tmp/log
      - name: sidecar
        image: busybox:1.31.0
        command: ["sh", "-c", "while true; do date >> /var/log/date.log; sleep 1; done"]
        volumeMounts:
        - name: log-data
          mountPath: /var/log
      volumes:
      - name: log-data
        emptyDir: {}
EOF

kubectl apply -f "$SCRIPT_DIR/../lab/pluto-deployment.yaml"
kubectl wait deployment pluto-deployment -n pluto --for=condition=Available --timeout=60s
