#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }

kubectl get storageclass fast >/dev/null 2>&1 || fail "StorageClass fast not found"
prov=$(kubectl get sc fast -o jsonpath='{.provisioner}')
[ "$prov" = "rancher.io/local-path" ] || fail "StorageClass fast provisioner must be rancher.io/local-path (got $prov)"
mode=$(kubectl get sc fast -o jsonpath='{.volumeBindingMode}')
[ "$mode" = "WaitForFirstConsumer" ] || fail "volumeBindingMode must be WaitForFirstConsumer (got $mode)"

kubectl -n storage get pvc data-pvc >/dev/null 2>&1 || fail "PVC storage/data-pvc not found"
sc=$(kubectl -n storage get pvc data-pvc -o jsonpath='{.spec.storageClassName}')
[ "$sc" = "fast" ] || fail "PVC storageClassName must be fast (got $sc)"
am=$(kubectl -n storage get pvc data-pvc -o jsonpath='{.spec.accessModes[0]}')
[ "$am" = "ReadWriteOnce" ] || fail "PVC accessMode must be ReadWriteOnce"
req=$(kubectl -n storage get pvc data-pvc -o jsonpath='{.spec.resources.requests.storage}')
[ "$req" = "500Mi" ] || fail "PVC size must be 500Mi (got $req)"

# wait up to 60s for pod and binding
for i in $(seq 1 30); do
  phase=$(kubectl -n storage get pvc data-pvc -o jsonpath='{.status.phase}' 2>/dev/null)
  podphase=$(kubectl -n storage get pod data-pod -o jsonpath='{.status.phase}' 2>/dev/null)
  [ "$phase" = "Bound" ] && [ "$podphase" = "Running" ] && break
  sleep 2
done
[ "$(kubectl -n storage get pvc data-pvc -o jsonpath='{.status.phase}')" = "Bound" ] || fail "PVC not Bound"
[ "$(kubectl -n storage get pod data-pod -o jsonpath='{.status.phase}')" = "Running" ] || fail "Pod data-pod not Running"

mp=$(kubectl -n storage get pod data-pod -o jsonpath='{.spec.containers[0].volumeMounts[?(@.name=="data")].mountPath}')
[ -z "$mp" ] && mp=$(kubectl -n storage get pod data-pod -o jsonpath='{.spec.containers[0].volumeMounts[0].mountPath}')
[ "$mp" = "/data" ] || fail "volume must be mounted at /data (got $mp)"

echo "PASS"
