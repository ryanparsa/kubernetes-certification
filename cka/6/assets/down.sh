#!/usr/bin/env bash
set -euo pipefail

kind delete cluster --name cka-lab
rm -rf /tmp/cka6-data

echo "Lab torn down."
