#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$SCRIPT_DIR/../course"

PASS=0
FAIL=0

echo "=== Check 1: etcd version file ==="
if [[ -f "$COURSE_DIR/etcd-version" ]] && grep -q "etcd Version:" "$COURSE_DIR/etcd-version"; then
  echo "PASS: etcd-version contains version info"
  PASS=$((PASS + 1))
else
  echo "FAIL: etcd-version file missing or does not contain 'etcd Version:'"
  FAIL=$((FAIL + 1))
fi

echo "=== Check 2: etcd snapshot file ==="
if [[ -s "$COURSE_DIR/etcd-snapshot.db" ]]; then
  echo "PASS: etcd-snapshot.db exists and is non-empty"
  PASS=$((PASS + 1))
else
  echo "FAIL: etcd-snapshot.db not found or is empty"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "Checks passed: $PASS/2"
[[ $FAIL -eq 0 ]] || exit 1
