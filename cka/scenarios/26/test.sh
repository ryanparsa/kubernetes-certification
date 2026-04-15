#!/usr/bin/env bash
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG="$DIR/kubeconfig"
export KUBECONFIG

fail() { echo "FAIL: $1"; exit 1; }

# Check CronJob existence
CJ=$(kubectl -n batch get cronjob db-cleanup -o json 2>/dev/null)
if [[ $? -ne 0 ]]; then
  fail "CronJob 'db-cleanup' not found in namespace 'batch'."
fi

# Check Schedule
SCHED=$(echo "$CJ" | jq -r '.spec.schedule')
if [[ "$SCHED" != "*/15 * * * *" ]]; then
  fail "Incorrect schedule: expected '*/15 * * * *', got '$SCHED'."
fi

# Check History Limits
SHL=$(echo "$CJ" | jq -r '.spec.successfulJobsHistoryLimit')
FHL=$(echo "$CJ" | jq -r '.spec.failedJobsHistoryLimit')
if [[ "$SHL" -ne 5 || "$FHL" -ne 2 ]]; then
  fail "Incorrect history limits: expected 5 success/2 failed, got $SHL/$FHL."
fi

# Check Restart Policy
RP=$(echo "$CJ" | jq -r '.spec.jobTemplate.spec.template.spec.restartPolicy')
if [[ "$RP" != "OnFailure" ]]; then
  fail "Incorrect restartPolicy: expected 'OnFailure', got '$RP'."
fi

echo "PASS"
