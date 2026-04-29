#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Define namespaces
NAMESPACES=("api-gateway-staging" "api-gateway-prod")

for ns in "${NAMESPACES[@]}"; do
  # 1. Remove the ConfigMap named api-gateway-autoscaler
  kubectl delete configmap api-gateway-autoscaler -n "$ns" --ignore-not-found

  # 2. Set the replicas of the Deployment api-gateway to 0
  kubectl scale deployment api-gateway --replicas=0 -n "$ns"

  # 3. Create a HorizontalPodAutoscaler named gateway
  # Minimum replicas: 2, Maximum replicas: 3, Target CPU utilization: 50%
  if ! kubectl get hpa gateway -n "$ns" &>/dev/null; then
    kubectl autoscale deployment api-gateway --name=gateway --min=2 --max=3 --cpu-percent=50 -n "$ns"
  else
    # If it already exists, patch it to ensure it matches requirements (idempotency)
    kubectl patch hpa gateway -n "$ns" --type='merge' -p '{"spec":{"minReplicas":2,"maxReplicas":3,"targetCPUUtilizationPercentage":50}}'
  fi
done
