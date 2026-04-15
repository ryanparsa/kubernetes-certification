#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

kind create cluster --name cka-task-26 --kubeconfig "$KUBECONFIG"

kubectl create ns batch

echo "Namespace 'batch' created for CronJob task."
