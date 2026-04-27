# File Templates

Exact boilerplate for every file in a lab. Replace `<exam>`, `<N>`, `<EXAM>` (uppercase) as needed.

---

## kind-config.yaml — single control-plane (default)

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: <exam>-lab-<N>
networking:
  ipFamily: ipv4
nodes:
  - role: control-plane
```

## kind-config.yaml — control-plane + worker

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: <exam>-lab-<N>
networking:
  ipFamily: ipv4
nodes:
  - role: control-plane
  - role: worker
```

## kind-config.yaml — CKS with audit logging

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: cks-lab-<N>
networking:
  ipFamily: ipv4
nodes:
  - role: control-plane
    extraMounts:
      - hostPath: /tmp/cks-lab-<N>-audit
        containerPath: /etc/kubernetes/audit
    kubeadmConfigPatches:
      - |
        kind: ClusterConfiguration
        apiServer:
          extraArgs:
            audit-log-path: /etc/kubernetes/audit/audit.log
            audit-policy-file: /etc/kubernetes/audit/policy.yaml
          extraVolumes:
            - name: audit
              hostPath: /etc/kubernetes/audit
              mountPath: /etc/kubernetes/audit
              readOnly: false
              pathType: DirectoryOrCreate
```

---

## setup.sh — minimal (no pre-seeded resources)

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$SCRIPT_DIR/../lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

echo ""
echo "Lab ready!"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
```

## setup.sh — with pre-seeded namespace + workload

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"

for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

mkdir -p "$SCRIPT_DIR/../lab"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
export KUBECONFIG="$KUBECONFIG_FILE"

# Pre-seed resources
kubectl apply -f "$SCRIPT_DIR/setup.yaml"

# Wait for workloads if needed
# kubectl rollout status deployment/<name> -n <ns> --timeout=60s

echo ""
echo "Lab ready!"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
```

---

## fix.sh — kubectl-apply solution

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

mkdir -p "$SCRIPT_DIR/../lab"

kubectl apply -f - <<EOF
apiVersion: v1
kind: <Kind>
metadata:
  name: <name>
  namespace: <namespace>
spec:
  ...
EOF

# Wait for resource to be ready
kubectl wait <resource>/<name> -n <namespace> --for=condition=Ready --timeout=60s
```

## fix.sh — file-output solution (e.g. etcd-info)

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

CONTROL_PLANE_NODE="$CLUSTER_NAME-control-plane"

mkdir -p "$SCRIPT_DIR/../lab"

# Extract values from cluster and write output file
cat <<EOF > "$SCRIPT_DIR/../lab/<output-file>"
Key: $(docker exec "$CONTROL_PLANE_NODE" <command>)
EOF
```

---

## check.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

python3 "$(dirname "$0")/_check.py"
```

---

## _check.py — Kubernetes object assertions

```python
#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    r = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return r.stdout.strip()

class Test<TitleNospaces>(unittest.TestCase):
    def test_<requirement>(self):
        val = kubectl("get", "<resource>", "<name>", "-n", "<ns>",
                      "-o", "jsonpath={.<field>}")
        self.assertEqual(val, "<expected>")

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## _check.py — file content assertions

```python
#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LAB_DIR = os.path.join(SCRIPT_DIR, "..", "lab")

LAB_ID = os.path.basename(os.path.dirname(SCRIPT_DIR))
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CONTROL_PLANE_NODE = f"{EXAM}-lab-{LAB_ID}-control-plane"

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

class Test<TitleNospaces>(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.info = {}
        path = os.path.join(LAB_DIR, "<output-file>")
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    if ":" in line:
                        k, v = line.split(":", 1)
                        cls.info[k.strip()] = v.strip()

    def test_file_exists(self):
        self.assertTrue(os.path.exists(os.path.join(LAB_DIR, "<output-file>")))

    def test_<field>(self):
        expected = run(f"docker exec {CONTROL_PLANE_NODE} <command>")
        self.assertEqual(self.info.get("<Key>"), expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

---

## cleanup.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"

kind delete cluster --name "$EXAM-lab-$LAB_ID"
rm -rf "$SCRIPT_DIR/../lab"
echo "Lab torn down."
```

---

## CI workflow (.github/workflows/<exam>-lab-<N>.yml)

```yaml
name: <EXAM> Lab <N>

on:
  push:
    paths: ['<exam>/<N>/**', '.github/workflows/<exam>-lab-<N>.yml']
  pull_request:
    paths: ['<exam>/<N>/**', '.github/workflows/<exam>-lab-<N>.yml']

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Create cluster
        uses: helm/kind-action@v1
        with:
          config: <exam>/<N>/assets/kind-config.yaml
          cluster_name: <exam>-lab-<N>

      - name: Apply solution
        run: bash <exam>/<N>/assets/fix.sh

      - name: Run checks
        run: bash <exam>/<N>/assets/check.sh

      - name: Tear down
        if: always()
        run: bash <exam>/<N>/assets/cleanup.sh
```

**Note:** The `helm/kind-action@v1` step creates the cluster AND sets `KUBECONFIG` automatically, so `fix.sh` and `check.sh` must also set `KUBECONFIG` internally (they do, via `export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"`) — but `kind-action` writes to a different path. Always include `export KUBECONFIG` inside each script rather than relying on the environment.
