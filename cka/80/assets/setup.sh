#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# Create the course directory on host
mkdir -p "$SCRIPT_DIR/course"

# Provision cluster
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
export KUBECONFIG="$KUBECONFIG_FILE"

# Create some pods in different namespaces
kubectl create ns project-a
kubectl create ns project-b

kubectl run pod-a1 -n project-a --image=nginx:1.23.1
kubectl run pod-a2 -n project-a --image=nginx:1.23.1
kubectl run pod-b1 -n project-b --image=redis:7.0.5
kubectl run pod-default -n default --image=busybox:1.35.0 -- sleep 3600

# Add user accounts-432 to kubeconfig
CERT_DIR=$(mktemp -d)
openssl genrsa -out "$CERT_DIR/user.key" 2048
openssl req -new -key "$CERT_DIR/user.key" -out "$CERT_DIR/user.csr" -subj "/CN=accounts-432"
openssl x509 -req -in "$CERT_DIR/user.csr" -signkey "$CERT_DIR/user.key" -out "$CERT_DIR/user.crt" -days 365

USER_CERT_B64=$(cat "$CERT_DIR/user.crt" | base64 | tr -d '\n')
kubectl config set-credentials accounts-432 --client-certificate-data="$USER_CERT_B64" --kubeconfig="$KUBECONFIG_FILE"

# Propagate kubeconfig to the control-plane node so kubectl commands inside work
docker cp "$KUBECONFIG_FILE" "$CLUSTER_NAME-control-plane:/root/.kube/config"

rm -rf "$CERT_DIR"

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
