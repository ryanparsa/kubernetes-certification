#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"
CLUSTER_NAME="cka-lab-80"

# 1. Write all pod names running in all namespaces, one per line, into /opt/course/1/pods.txt
docker exec "$CLUSTER_NAME-control-plane" sh -c "kubectl get pods -A -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' > /opt/course/1/pods.txt"

# 2. Write all running container image names from all pods in all namespaces, one per line (deduplicated), into /opt/course/1/containers.txt
docker exec "$CLUSTER_NAME-control-plane" sh -c "kubectl get pods -A -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u > /opt/course/1/containers.txt"

# 3. Write the name of the current context into /opt/course/1/context
docker exec "$CLUSTER_NAME-control-plane" sh -c "kubectl config current-context > /opt/course/1/context"

# 4. Write the client certificate of user accounts-432 (decode it and write only the certificate string) into /opt/course/1/cert
docker exec "$CLUSTER_NAME-control-plane" sh -c "kubectl config view --raw -o jsonpath='{.users[?(@.name==\"accounts-432\")].user.client-certificate-data}' | base64 -d > /opt/course/1/cert"
