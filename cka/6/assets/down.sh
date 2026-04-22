#!/usr/bin/env bash
set -euo pipefail

kind delete cluster --name cka-lab

echo "Lab torn down."
