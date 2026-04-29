#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="${KUBECONFIG:-$SCRIPT_DIR/../lab/kubeconfig.yaml}"

# 1. Create pods and services
kubectl run consumer --image=nginx --labels="run=consumer"
kubectl expose pod consumer --port=80

kubectl run producer --image=nginx --labels="run=producer"
kubectl expose pod producer --port=80

kubectl run web --image=nginx --labels="run=web"
kubectl expose pod web --port=80

# 2. Wait for pods to be ready
kubectl wait --for=condition=Ready pod/consumer pod/producer pod/web --timeout=60s

# 3. Create the NetworkPolicy
cat <<NP_EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: limit-consumer
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: consumer
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          run: producer
NP_EOF
