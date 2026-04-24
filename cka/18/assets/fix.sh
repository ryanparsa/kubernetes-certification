#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/kubeconfig.yaml}"

kubectl -n lima-control patch cm control-config --type merge -p '{
  "data": {
    "DNS_1": "kubernetes.default.svc.cluster.local",
    "DNS_2": "department.lima-workload.svc.cluster.local",
    "DNS_3": "section100.section.lima-workload.svc.cluster.local",
    "DNS_4": "1-2-3-4.kube-system.pod.cluster.local"
  }
}'

kubectl -n lima-control rollout restart deploy controller
kubectl -n lima-control rollout status deploy controller
