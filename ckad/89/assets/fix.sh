#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# Scale down Deployment to 0
kubectl scale deployment neptune-10ab -n neptune --replicas=0

# Wait for pods to be terminated
kubectl wait pod -l app=neptune-10ab -n neptune --for=delete --timeout=60s || true

# Annotate Deployment for maintenance protection
kubectl annotate deployment neptune-20ab -n neptune admission.datree.io/warn="true" --overwrite

# Add delete protection
kubectl patch deployment neptune-20ab -n neptune -p '{"metadata":{"finalizers":["kubernetes.io/prevent-deletion"]}}' --type=merge
kubectl annotate deployment neptune-20ab -n neptune kubectl.kubernetes.io/last-applied-configuration='{"apiVersion":"apps/v1","kind":"Deployment","metadata":{"name":"neptune-20ab","namespace":"neptune"}}' --overwrite
