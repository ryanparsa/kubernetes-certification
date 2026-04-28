#!/usr/bin/env bash
set -euo pipefail

# 1. Check dependencies
for cmd in docker; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "$cmd is not installed."
        exit 1
    fi
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 2. Create cluster
# N/A - This task is host-based

# 3. Apply pre-existing workloads
# N/A

# 4. Wait for deployments
# N/A

# 5. Create the output directory
mkdir -p "$SCRIPT_DIR/../lab"

# 6. Copy task assets
# N/A

# 7. Print summary
echo "Lab ready! Solve the task on the host machine."
