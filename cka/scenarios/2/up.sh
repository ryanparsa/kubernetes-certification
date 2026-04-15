#!/usr/bin/env bash
set -euo pipefail
CLUSTER=cka-task-2
NODE="${CLUSTER}-control-plane"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

kind create cluster --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
kubectl wait --for=condition=Ready node --all --timeout=180s

# Sabotage the control plane:
# 1) kube-apiserver: point --etcd-servers at a bogus address
# 2) kube-controller-manager: request impossibly high CPU
docker exec "$NODE" sh -c '
set -e
sed -i "s|--etcd-servers=https://127.0.0.1:2379|--etcd-servers=https://192.168.99.99:2380|" /etc/kubernetes/manifests/kube-apiserver.yaml
# add a giant cpu request to kube-controller-manager
python3 - <<PY
import re,sys
p="/etc/kubernetes/manifests/kube-controller-manager.yaml"
s=open(p).read()
if "resources:" in s and "cpu: 200m" not in s:
    s=re.sub(r"resources:\s*\{\}", "resources:\n      requests:\n        cpu: \"99\"", s)
elif "resources: {}" in s:
    s=s.replace("resources: {}", "resources:\n      requests:\n        cpu: \"99\"")
else:
    s=s.replace("name: kube-controller-manager", "name: kube-controller-manager\n    resources:\n      requests:\n        cpu: \"99\"", 1)
open(p,"w").write(s)
PY
' || {
  # python3 may not exist; fall back to sed
  docker exec "$NODE" sh -c '
    sed -i "s|resources: {}|resources:\n      requests:\n        cpu: \"99\"|" /etc/kubernetes/manifests/kube-controller-manager.yaml
  '
}

echo
echo "Control plane has been sabotaged. kubectl will start failing within ~30s."
echo
echo "READY. Run:"
echo "  export KUBECONFIG=$KUBECONFIG"
echo "  cat $DIR/task.md"
