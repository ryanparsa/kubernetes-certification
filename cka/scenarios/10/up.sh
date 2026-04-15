#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-10
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

# Break in-cluster DNS by scaling CoreDNS to zero
kubectl -n kube-system scale deployment coredns --replicas=0
kubectl -n kube-system wait --for=delete pod -l k8s-app=kube-dns --timeout=60s || true

# Seed a target Service so the user has something to dig for
kubectl create namespace probe
kubectl -n probe create deployment web --image=nginx:1.27-alpine
kubectl -n probe expose deployment web --port=80

echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
