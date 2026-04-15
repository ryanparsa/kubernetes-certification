#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$DIR/kubeconfig"

fail() { echo "FAIL: $*"; exit 1; }
J() { kubectl -n app get pod app-pod -o jsonpath="$1" 2>/dev/null; }

kubectl -n app get pod app-pod >/dev/null 2>&1 || fail "Pod app/app-pod not found"
[ "$(J '{.status.phase}')" = "Running" ] || fail "Pod not Running"

img=$(J '{.spec.containers[0].image}')
[ "$img" = "nginx:1.27-alpine" ] || fail "container image must be nginx:1.27-alpine"

# verify volume mounts
cfg=$(kubectl -n app get pod app-pod -o jsonpath='{.spec.containers[0].volumeMounts[?(@.mountPath=="/etc/config")].name}')
sec=$(kubectl -n app get pod app-pod -o jsonpath='{.spec.containers[0].volumeMounts[?(@.mountPath=="/etc/secret")].name}')
[ -n "$cfg" ] || fail "missing volume mount at /etc/config"
[ -n "$sec" ] || fail "missing volume mount at /etc/secret"

# verify the volumes themselves point at the right resources
cm=$(kubectl -n app get pod app-pod -o jsonpath="{.spec.volumes[?(@.name==\"$cfg\")].configMap.name}")
[ "$cm" = "app-config" ] || fail "/etc/config volume must come from configMap app-config (got $cm)"

sname=$(kubectl -n app get pod app-pod -o jsonpath="{.spec.volumes[?(@.name==\"$sec\")].secret.secretName}")
[ "$sname" = "app-secret" ] || fail "/etc/secret volume must come from secret app-secret (got $sname)"

mode=$(kubectl -n app get pod app-pod -o jsonpath="{.spec.volumes[?(@.name==\"$sec\")].secret.defaultMode}")
[ "$mode" = "256" ] || fail "secret volume defaultMode must be 0400 / 256 (got $mode)"

# env from refs
ll=$(kubectl -n app get pod app-pod -o jsonpath='{.spec.containers[0].env[?(@.name=="LOG_LEVEL")].valueFrom.configMapKeyRef.key}')
[ "$ll" = "LOG_LEVEL" ] || fail "env LOG_LEVEL must come from configMapKeyRef LOG_LEVEL"

dp=$(kubectl -n app get pod app-pod -o jsonpath='{.spec.containers[0].env[?(@.name=="DB_PASSWORD")].valueFrom.secretKeyRef.key}')
[ "$dp" = "DB_PASSWORD" ] || fail "env DB_PASSWORD must come from secretKeyRef DB_PASSWORD"

# inside-pod confirmation
kubectl -n app exec app-pod -- test -f /etc/config/LOG_LEVEL || fail "/etc/config/LOG_LEVEL not present in pod"
kubectl -n app exec app-pod -- test -f /etc/secret/DB_PASSWORD || fail "/etc/secret/DB_PASSWORD not present in pod"

echo "PASS"
