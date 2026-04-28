#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

kubectl scale sts o3db -n project-c13 --replicas 1

kubectl rollout status statefulset/o3db -n project-c13 --timeout=60s

# Ensure the status is fully updated before finishing
kubectl wait --for=jsonpath='{.status.readyReplicas}'=1 sts/o3db -n project-c13 --timeout=60s
