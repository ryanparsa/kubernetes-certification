#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ID="$(basename "$TASK_DIR")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$TASK_DIR/lab/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
mkdir -p "$TASK_DIR/lab"
# Create a local directory that will be mounted into the control-plane node
mkdir -p "$SCRIPT_DIR/course"

if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
else
  kind get kubeconfig --name "$CLUSTER_NAME" > "$KUBECONFIG_FILE"
fi

export KUBECONFIG="$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads
kubectl create ns project-a --dry-run=client -o yaml | kubectl apply -f -
kubectl create ns project-b --dry-run=client -o yaml | kubectl apply -f -

kubectl run pod-a1 -n project-a --image=nginx:1.23.1 --overrides='{"spec": {"terminationGracePeriodSeconds": 0}}' --dry-run=client -o yaml | kubectl apply -f -
kubectl run pod-a2 -n project-a --image=nginx:1.23.1 --overrides='{"spec": {"terminationGracePeriodSeconds": 0}}' --dry-run=client -o yaml | kubectl apply -f -
kubectl run pod-b1 -n project-b --image=redis:7.0.5 --overrides='{"spec": {"terminationGracePeriodSeconds": 0}}' --dry-run=client -o yaml | kubectl apply -f -
kubectl run pod-default -n default --image=busybox:1.35.0 --overrides='{"spec": {"terminationGracePeriodSeconds": 0}}' --dry-run=client -o yaml -- sleep 3600 | kubectl apply -f -

# Add user accounts-432 to kubeconfig
CERT_DIR=$(mktemp -d)
openssl genrsa -out "$CERT_DIR/user.key" 2048
openssl req -new -key "$CERT_DIR/user.key" -out "$CERT_DIR/user.csr" -subj "/CN=accounts-432"
openssl x509 -req -in "$CERT_DIR/user.csr" -signkey "$CERT_DIR/user.key" -out "$CERT_DIR/user.crt" -days 365

# Update host kubeconfig
kubectl config set-credentials accounts-432 --client-certificate="$CERT_DIR/user.crt" --client-key="$CERT_DIR/user.key" --embed-certs=true

# Update internal kubeconfig in the control-plane node
docker cp "$CERT_DIR/user.crt" "$CLUSTER_NAME-control-plane:/tmp/user.crt"
docker exec "$CLUSTER_NAME-control-plane" kubectl config set-credentials accounts-432 --client-certificate=/tmp/user.crt --embed-certs=true --kubeconfig=/etc/kubernetes/admin.conf
docker exec "$CLUSTER_NAME-control-plane" rm /tmp/user.crt

rm -rf "$CERT_DIR"

echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
