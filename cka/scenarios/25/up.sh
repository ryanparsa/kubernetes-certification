#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-25 --kubeconfig "$KUBECONFIG"

kubectl create ns restricted
kubectl create ns external-world

# Deploy "external" services
kubectl -n external-world run database --image=nginx:1.27-alpine --labels=app=db
kubectl -n external-world expose pod database --port=5432 --target-port=80

echo "Environment for Egress NetworkPolicy task created."
