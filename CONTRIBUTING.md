# Contributing

git config core.hooksPath .githooks

## Repository Layout

```
kubernetes-certification/
├── kcna/         # KCNA study material
├── kcsa/         # KCSA study material
├── ckad/         # CKAD labs
├── cka/          # CKA labs
├── cks/          # CKS labs
├── ref/          # Shared reference sheets (all exams)
└── prompts/      # AI prompts
```

## Certification Types

**Lab exams - CKA, CKAD, CKS**

Each lab is numbered by its question number. Labs are added incrementally as they are worked through.

```
<exam>/<N>/
├── README.md     # Question only
├── answer.md     # Reference answer + checklist
└── assets/       # Setup, teardown, validation scripts
```

**Study-only exams - KCNA, KCSA**

Contains exam overview, practice Q&A, a domain checklist, and a resources list.

```
<exam>/
├── README.md
├── <exam>-assessment-bank.md
├── <exam>-exam-checklist.md
└── resources.md
```

---

## Prerequisites

| Tool                              | Purpose                                   | Install                                                        |
|-----------------------------------|-------------------------------------------|----------------------------------------------------------------|
| `docker` / `orbstack` / `podman`  | Container runtime (required by kind)      | <https://docs.docker.com/get-docker/> - <https://orbstack.dev> - <https://podman.io> |
| `kind`                            | Local Kubernetes clusters via containers  | <https://kind.sigs.k8s.io/docs/user/quick-start/>              |
| `limactl`                         | Local Kubernetes clusters via VMs         | <https://lima-vm.io/>                                          |
| `kubectl`                         | Interacts with the cluster                | <https://kubernetes.io/docs/tasks/tools/>                      |
| `python3`                         | Runs `_check.py` validation suite         | <https://www.python.org/downloads/> (3.8+)                     |

---

## Choosing a Cluster Tool

Both `kind` and `lima` can provision a local Kubernetes cluster for a lab. Pick based on what the task actually needs.

**kind** spins up nodes as Docker containers. It starts in seconds, tears down cleanly, and runs inside GitHub Actions with no extra setup. Use it for anything that stays at the Kubernetes API level - workloads, RBAC, networking, storage, scheduling. kind works with Docker, OrbStack, and Podman as the container runtime.

**lima** runs real VMs with full systemd and an OS package manager. Use it when the task requires interacting below the Kubernetes API - installing or upgrading Kubernetes packages with `apt`, running `kubeadm join` to attach a new node, restarting `kubelet` via `systemctl`, or anything that touches the node OS directly. These scenarios need a real kernel and cannot run in CI.

If you're unsure, start with kind. Switch to lima only when kind can't replicate what the task requires.

### kind in a lab

Add a `kind-config.yaml` to `assets/` defining the cluster topology. `setup.sh` creates the cluster and writes a kubeconfig; `cleanup.sh` deletes it.

```bash
# setup.sh (kind portion)
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"
kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"
export KUBECONFIG="$KUBECONFIG_FILE"
# apply seed resources here
mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready! Run: export KUBECONFIG=$KUBECONFIG_FILE"
```

```bash
# cleanup.sh (kind portion)
kind delete cluster --name "$CLUSTER_NAME"
rm -rf "$SCRIPT_DIR/../lab"
```

`fix.sh` and `check.sh` reference the kubeconfig via `export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"`.

A minimal `kind-config.yaml`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: <exam>-lab-<N>
nodes:
  - role: control-plane
  - role: worker
```

Add more nodes or extra configuration only when the task requires it.

### lima in a lab

Add VM spec files (`control-plane.yaml`, optionally `worker.yaml`) and provisioning scripts (`provision-control-plane.sh`, optionally `provision-worker.sh`) to `assets/`. `setup.sh` starts the VMs, runs provisioning inside them, and extracts the kubeconfig into `lab/`. For node-level work during the lab, shell into VMs via `limactl shell`.

```bash
# setup.sh (lima portion)
CP_NAME="$CLUSTER_NAME-cp"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
mkdir -p "$SCRIPT_DIR/../lab"

limactl start --name "$CP_NAME" "$SCRIPT_DIR/control-plane.yaml"
limactl copy "$SCRIPT_DIR/provision-control-plane.sh" "$CP_NAME:/tmp/provision.sh"
limactl shell "$CP_NAME" sudo bash /tmp/provision.sh

# repeat for worker if multi-node

limactl copy "$CP_NAME:/etc/kubernetes/admin.conf" "$KUBECONFIG_FILE"
CP_IP=$(limactl shell "$CP_NAME" hostname -I | awk '{print $1}')
sed -i.bak "s|server: https://.*:6443|server: https://$CP_IP:6443|" "$KUBECONFIG_FILE"
rm -f "${KUBECONFIG_FILE}.bak"

echo "Lab ready!"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
echo "  limactl shell $CP_NAME"
```

```bash
# cleanup.sh (lima portion)
limactl delete --force "$CLUSTER_NAME-cp" "$CLUSTER_NAME-worker" 2>/dev/null || true
rm -rf "$SCRIPT_DIR/../lab"
```

Node-level commands in `fix.sh` run through `limactl shell`:

```bash
limactl shell "$CP_NAME" sudo kubeadm ...
limactl shell "$WORKER_NAME" sudo systemctl restart kubelet
```

---

## Lab Directory Layout

```
<exam>/<N>/
├── README.md
├── answer.md
├── assets/
│   ├── setup.sh
│   ├── cleanup.sh
│   ├── fix.sh
│   ├── check.sh
│   └── _check.py     # optional - only for complex validation logic
└── lab/              # generated by setup.sh (git-ignored)
```

`assets/` may contain additional environment-specific files (cluster configs, VM specs, seed manifests, etc.) depending on how the lab provisions its cluster.

---

## File Formats

### `README.md` - question only

````markdown
# Question <N>

> **Solve this question on:** `<exam>-lab-<N>`

<Task description - exactly as the exam would phrase it.>

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
````

Do not include the answer or checklist here - those live in `answer.md`.

### `answer.md` - reference answer + checklist

````markdown
## Answer

**Reference:** <kubernetes.io docs link>

### <Step heading>

```bash
kubectl ...
```

```yaml
# lab/<filename>.yaml
apiVersion: v1
kind: <Kind>
...
```

## Checklist (Score: 0/<N>)

- [ ] <Requirement 1>
- [ ] <Requirement 2>
````

### `setup.sh`

Provisions the cluster and seeds any required resources. Use the following variable boilerplate so the cluster name is always derived from the directory path:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
CLUSTER_NAME="$EXAM-lab-$LAB_ID"

# provision cluster, apply seed resources

mkdir -p "$SCRIPT_DIR/../lab"
echo "Lab ready!"
```

### `cleanup.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ID="$(basename "$(dirname "$SCRIPT_DIR")")"
EXAM="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"

# tear down cluster

rm -rf "$SCRIPT_DIR/../lab"
echo "Lab torn down."
```

### `fix.sh`

Reproduces the complete solution from a clean cluster state. Use whatever tools the task requires - `kubectl apply`, `kubectl patch`, `kubectl delete`, `kubectl create`, or any other Linux command. The only constraint is that it must be idempotent (safe to run more than once).

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# implement the solution here
```

### `check.sh`

Write assertions directly in bash. For complex logic (OR conditions, JSON parsing, cross-resource checks) delegate to `_check.py`:

```bash
#!/usr/bin/env bash
python3 "$(dirname "$0")/_check.py"
```

### `_check.py` (optional)

Only add this file when `check.sh` logic becomes complex. One `TestCase` class, one `test_` method per checklist item. Use `jsonpath` - avoid parsing text output.

```python
#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class Test<LabName>(unittest.TestCase):
    def test_<requirement>(self):
        value = kubectl("get", "<resource>", "<name>", "-n", "<ns>", "-o", "jsonpath={.<field>}")
        self.assertEqual(value, "expected")

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

---

## Study Material Structure

| File | Purpose |
|---|---|
| `README.md` | Exam overview and domain weights |
| `<exam>-assessment-bank.md` | Practice Q&A |
| `<exam>-exam-checklist.md` | Domain-by-domain prep checklist |
| `resources.md` | Curated learning resources |

---

## Conventions

| Convention | Rule |
|---|---|
| Cluster name | `<exam>-lab-<N>` |
| Kubernetes Version | All labs, manifests, and solutions must target **Kubernetes v1.35**. Do not use deprecated APIs. |
| Relative Paths | All file paths in `README.md`, `answer.md`, and scripts must be relative to the lab directory (e.g., `assets/setup.sh`). |
| Manifests | Written to `lab/` while solving; `lab/` is git-ignored |
| `fix.sh` | Idempotent - uses `kubectl apply`, not `kubectl create` |
| `kubectl wait` | Use in any `.sh` file after applying resources to block until the expected state is reached: `kubectl wait <resource> <name> -n <namespace> --for=condition=Ready --timeout=60s` |
| `_check.py` class name | `Test<DescriptiveLabName>` matching the question title |
| Checklist score | Start at `0/<N>` - update to `<N>/<N>` once all checks pass |
| Multiple approaches | Document all valid approaches in `answer.md`; pick the simpler one for `fix.sh` |

---

## Workflow

1. **Set up**: run `setup.sh`, export `KUBECONFIG`, confirm nodes are `Ready`.
2. **Read**: study `README.md` - identify resources, namespaces, and constraints before touching the cluster.
3. **Explore**: `kubectl get all -A` and related commands to understand the current state.
4. **Solve**: implement the solution; save manifests under `lab/`; write `fix.sh` and `check.sh` as you go.
5. **Verify**: run `check.sh` - do not mark the lab done until every check passes.
6. **Tear down**: run `cleanup.sh`.

---

## Exam-Specific Notes

- **KCNA / KCSA**: assessment bank, checklist, and resources - no lab scripts or CI.
- **CKAD**: may pre-seed namespaces, resource quotas, or broken workloads in `setup.sh`.
- **CKA**: use multi-node topologies when the task involves scheduling or node management.
- **CKS**: may need extra mounts and kubeadm config patches in the cluster config (audit logging, encryption).

---

## CI

Every lab whose environment can run inside a GitHub Actions runner must have `.github/workflows/<exam>-lab-<N>.yml`. Labs that require a real VM or local tooling are excluded - do not add a workflow for them.

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
    steps:
      - uses: actions/checkout@v4

      - name: Create cluster
        uses: helm/kind-action@v1
        with:
          config: <exam>/<N>/assets/<cluster-config>.yaml
          cluster_name: <exam>-lab-<N>

      - name: Apply solution
        run: bash <exam>/<N>/assets/fix.sh

      - name: Run checks
        run: bash <exam>/<N>/assets/check.sh

      - name: Tear down
        if: always()
        run: bash <exam>/<N>/assets/cleanup.sh
```

The tear-down step must be `if: always()` so the cluster is deleted even when checks fail.

---

## Submitting a Contribution

- **Branch**: `add-<exam>-lab-<N>`.
- **Commit**: `<exam>/<N>: <short description>`.
- **PR title**: `<exam>/<N>: <short description>`.
- **PR description**: include the checklist from `answer.md` so reviewers see the scoring criteria at a glance.
- Ensure CI passes before requesting review.
