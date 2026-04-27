#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/../lab/kubeconfig.yaml" ]; then
  export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"
fi

# Update ConfigMap with correct DNS FQDN values
kubectl -n lima-control patch configmap control-config \
  --type=merge \
  -p '{
    "data": {
      "DNS_1": "kubernetes.default.svc.cluster.local",
      "DNS_2": "department.lima-workload.svc.cluster.local",
      "DNS_3": "section100.section.lima-workload.svc.cluster.local",
      "DNS_4": "1-2-3-4.kube-system.pod.cluster.local"
    }
  }'

# Restart the Deployment to pick up the new ConfigMap values
kubectl -n lima-control rollout restart deployment controller

# Wait for rollout to complete
kubectl -n lima-control rollout status deployment controller --timeout=120s
