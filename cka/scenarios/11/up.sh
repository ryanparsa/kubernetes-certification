#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-11
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

command -v helm >/dev/null 2>&1 || { echo "helm not installed (brew install helm)"; exit 1; }

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace platform

# Create Helm chart structure
CHART_DIR="$DIR/charts/web"
mkdir -p "$CHART_DIR/templates"

cat > "$CHART_DIR/Chart.yaml" <<EOF
apiVersion: v2
name: web
version: 0.1.0
EOF

cat > "$CHART_DIR/values.yaml" <<EOF
replicaCount: 1
image: nginx:1.27-alpine
serviceType: ClusterIP
EOF

cat > "$CHART_DIR/templates/deployment.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector: { matchLabels: { app: {{ .Release.Name }} } }
  template:
    metadata: { labels: { app: {{ .Release.Name }} } }
    spec:
      containers:
      - name: web
        image: {{ .Values.image }}
        ports: [{ containerPort: 80 }]
EOF

cat > "$CHART_DIR/templates/service.yaml" <<EOF
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  type: {{ .Values.serviceType }}
  selector: { app: {{ .Release.Name }} }
  ports: [{ port: 80, targetPort: 80 }]
EOF

echo
echo "Local chart available at: $CHART_DIR"
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
