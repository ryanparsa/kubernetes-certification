# CKA Lab Setup — Generic Prompt

Use this prompt with any CKA question directory. When given a directory number `N`, read `cka/N/readme.md`, understand what the task requires, and set up a complete local kind-based lab so the user can practice from the correct starting state.

---

## Step 1: Analyze the Task Before Creating Anything

Read **both** the task description and the **Answer section** of `cka/N/readme.md` carefully. The answer section often reveals resource details (replica counts, resource requests, label values) that the task description alone does not. Answer these questions before writing any files:

1. **What namespaces must already exist?** The task will name them explicitly.
2. **What resources must already exist?** Look at what the task description and answer assume is already running — Deployments, Services, ConfigMaps, Pods, ServiceAccounts, etc. Use the answer's `kubectl get` output to infer replica counts, resource requests, and label names. Only create the *starting state*, not the solution.
3. **Does the task write output to files?** (e.g. "write the result to `cka/N/course/foo.txt`") → if yes, `up.sh` must `mkdir -p` the `cka/N/course/` directory, and `down.sh` must remove it.
4. **Does the task need a kubeconfig file at a specific path?** → create `task-kubeconfig.yaml` and copy it in `up.sh`.
5. **Does the task involve scheduling, node roles, or taints?** → the cluster needs at least one worker node in addition to the control-plane.
6. **Are any resources intentionally broken or misconfigured?** → apply them in that broken state.

---

## Step 2: Create the Lab Files

### `cka/N/assets/kind-config.yaml`

> For complex cluster requirements (multi-node, port mappings, extra mounts, etc.), refer to the kind docs:
> - https://kind.sigs.k8s.io/docs/user/quick-start/
> - https://kind.sigs.k8s.io/docs/user/configuration/

Default — single control-plane only:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: cka-lab
nodes:
- role: control-plane
```

Add a worker node when the task involves:
- Scheduling pods on specific node types (controlplane vs worker)
- Node taints, node selectors, or node affinity
- DaemonSets where node count matters
- Any mention of "worker node" or "node1" in the task

```yaml
# with one worker node
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: cka-lab
nodes:
- role: control-plane
- role: worker
```

---

### `cka/N/assets/<workload>.yaml`

Create one or more YAML manifests for all pre-existing resources the task assumes. Apply them in `up.sh`.

Common patterns to watch for in the readme:
- A Deployment or Pod already running → manifest + apply in `up.sh`
- A ConfigMap or Secret already existing (possibly with wrong/placeholder values) → manifest + apply
- A Service (regular or headless) already in place → manifest + apply
- A Namespace → create it before applying other resources
- Pods that need `hostname` and `subdomain` fields set → include those fields in the manifest
- Resources that are intentionally broken or misconfigured → apply them in that state

**Container image:** Use `nginx:alpine` for generic web/api workloads and `busybox` for utility/data workloads, unless the task names a specific image.

> **Rule:** Only create the starting state the task assumes. Do not create the resources the user is supposed to create as part of solving the task.

---

### `cka/N/assets/task-kubeconfig.yaml` *(only if the task involves a kubeconfig file)*

> **Naming rule:** Never name a tracked file starting with `kubeconfig` — the root `.gitignore` has a `kubeconfig*` rule that will silently suppress it. Always use `task-kubeconfig.yaml`.

A synthetic kubeconfig matching the exam scenario — correct contexts, users, and embedded cert data. The cluster server address can be fake (`https://10.30.110.30:6443`) since the task is about reading the file, not connecting. Copy it to `cka/N/course/kubeconfig` in `up.sh`.

---

### `cka/N/assets/up.sh`

Fully automated — zero manual steps for the user.

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Check dependencies
for cmd in kind kubectl docker; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' not found"; exit 1; }
done

# 2. Create cluster
kind create cluster --config "$SCRIPT_DIR/kind-config.yaml" --kubeconfig "$KUBECONFIG_FILE"

# 3. Apply pre-existing workloads (remove if not needed)
kubectl apply --kubeconfig "$KUBECONFIG_FILE" -f "$SCRIPT_DIR/<workload>.yaml"

# 4. Wait for deployments to be ready (adapt names; remove if no Deployments)
#    Use rollout status — NOT kubectl wait pod --all, which fails before pods exist.
for deploy in <name-1> <name-2>; do
  kubectl rollout status --kubeconfig "$KUBECONFIG_FILE" -n <namespace> \
    deployment/"$deploy" --timeout=120s
done

# 5. Create the course/ output directory (remove if the task writes no output files)
mkdir -p "$SCRIPT_DIR/../course"

# 6. Copy task kubeconfig into course/ (remove if the task has no kubeconfig scenario)
cp "$SCRIPT_DIR/task-kubeconfig.yaml" "$SCRIPT_DIR/../course/kubeconfig"

# 7. Print summary — always use export style, never --kubeconfig
echo ""
echo "Lab ready!"
echo ""
echo "Run this to set your kubeconfig:"
echo "  export KUBECONFIG=$KUBECONFIG_FILE"
```

Adapt the script: remove any step that does not apply (no workloads, no `course/` dir, no kubeconfig copy).

**Important:** Always end `up.sh` with an `export KUBECONFIG=...` instruction printed to the user. Never use `--kubeconfig` flags in the printed instructions.

Make the script executable.

---

### `cka/N/assets/down.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

kind delete cluster --name cka-lab

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf "$SCRIPT_DIR/../course"

echo "Lab torn down."
```

The `rm -rf` on `course/` is safe — no error if it doesn't exist. Make executable.

---

## Step 3: Adapt `cka/N/readme.md`

The readme is based on the killer.sh environment. You are allowed to edit it to match the local lab. Update:
- Node/host references: `ssh cka9412` lines → remove entirely
- Shell prompts in code blocks: `➜ candidate@cka2556:~$ ` → strip the prompt prefix, keep only the command
- Shortened prompts: `➜ ` at the start of a command line → remove
- File paths: `/opt/course/N/foo` → `cka/N/course/foo`
- Any other environmental detail that doesn't apply locally

Do **not** change the meaning, logic, or solution of the task itself.

---

## Step 4: Update Repo Files

### `.gitignore` (repo root)

Add `cka/N/course/` under the Kubernetes-specific section if the task writes output files. The runtime `cka/N/assets/kubeconfig.yaml` is already covered by the existing `kubeconfig*` rule.

### `cka/README.md`

After everything is created and verified, update the **Lab** column for directory `N` from empty to `Ready`.

---

## Step 5: Verify the Lab

```bash
# Start the lab
bash cka/N/assets/up.sh

# Set kubeconfig as printed by up.sh
export KUBECONFIG=cka/N/assets/kubeconfig.yaml

# Cluster is up
kubectl get nodes

# All pre-existing resources are in place
# (check the specific namespaces, deployments, services, etc. the task assumes)
kubectl get all -A

# Tear down
bash cka/N/assets/down.sh
# Confirm course/ is gone and cluster is deleted
```

Verify the **starting state** matches what the task description assumes — not the solution.
