#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check PV
PV=$(kubectl get pv manual-pv -o jsonpath='{.status.phase}' 2>/dev/null)
if [[ "$PV" != "Bound" ]]; then
  fail "PV 'manual-pv' is not Bound (Phase: $PV)."
fi

# Check PVC
PVC=$(kubectl get pvc manual-pvc -o jsonpath='{.status.phase}' 2>/dev/null)
if [[ "$PVC" != "Bound" ]]; then
  fail "PVC 'manual-pvc' is not Bound."
fi

# Check Pod
POD=$(kubectl get pod storage-pod -o jsonpath='{.status.phase}' 2>/dev/null)
if [[ "$POD" != "Running" ]]; then
  fail "Pod 'storage-pod' is not Running."
fi

# Check Content
CONTENT=$(kubectl exec storage-pod -- cat /usr/share/nginx/html/index.html 2>/dev/null)
if [[ "$CONTENT" != "hello from node" ]]; then
  fail "Pod is not correctly mounting the hostPath volume (content mismatch)."
fi

echo "PASS"
