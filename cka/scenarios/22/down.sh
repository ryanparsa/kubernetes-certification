#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind delete cluster --name cka-task-22
rm -f "$KUBECONFIG" "$DIR/john.key" "$DIR/john.csr"
