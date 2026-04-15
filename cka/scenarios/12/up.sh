#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-12
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

kubectl create namespace ops

# Create Kustomize structure
K8S_DIR="$DIR/k8s"
mkdir -p "$K8S_DIR/base" "$K8S_DIR/overlays/prod"

cat > "$K8S_DIR/base/deployment.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 1
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      containers:
      - name: api
        image: nginx:1.27-alpine
EOF

cat > "$K8S_DIR/base/kustomization.yaml" <<EOF
resources:
- deployment.yaml
EOF

cat > "$K8S_DIR/overlays/prod/kustomization.yaml" <<'EOF'
namespace: ops
resources:
- ../../base
# TODO: add a patch that scales replicas to 4
EOF

echo
echo "Kustomize project laid out at: $K8S_DIR"
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
