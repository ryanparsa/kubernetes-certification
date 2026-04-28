#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

BASE="$SCRIPT_DIR/../lab/api-gateway/base"
STAGING="$SCRIPT_DIR/../lab/api-gateway/staging"
PROD="$SCRIPT_DIR/../lab/api-gateway/prod"

# Step 1+2: Rewrite base/api-gateway.yaml - remove ConfigMap, add HPA
cat > "$BASE/api-gateway.yaml" <<'EOF'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 2
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  selector:
    matchLabels:
      id: api-gateway
  template:
    metadata:
      labels:
        id: api-gateway
    spec:
      serviceAccountName: api-gateway
      containers:
      - image: httpd:2-alpine
        name: httpd
        resources:
          requests:
            cpu: 100m
EOF

# Step 1: Remove ConfigMap patch from staging/api-gateway.yaml, keep Deployment label
cat > "$STAGING/api-gateway.yaml" <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  labels:
    env: staging
EOF

# Step 3: Override maxReplicas in prod, remove ConfigMap patch
cat > "$PROD/api-gateway.yaml" <<'EOF'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
spec:
  maxReplicas: 6
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  labels:
    env: prod
EOF

# Step 4: Apply staging and prod
kubectl kustomize "$STAGING" | kubectl apply -f -
kubectl kustomize "$PROD" | kubectl apply -f -

# Step 4 (cont.): Delete the remote ConfigMaps that are no longer in the Kustomize config
kubectl delete configmap horizontal-scaling-config -n api-gateway-staging --ignore-not-found
kubectl delete configmap horizontal-scaling-config -n api-gateway-prod --ignore-not-found
