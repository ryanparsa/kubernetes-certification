# CKA Lab Conventions

## Cluster Tool Selection
- Use kind for Kubernetes API-level tasks (workloads, RBAC, networking, storage, scheduling).
- Use lima when the task requires OS-level access: apt installs, kubeadm join, systemctl, etcdctl inside the node.
- cka/8 is the canonical multi-node lima lab template (control-plane + worker VMs).
- cka/24 (etcd snapshot) uses lima -- single control-plane VM, no worker.

## lima Lab Pattern
- VM spec: `assets/control-plane.yaml` (Ubuntu 24.04, cpus:2, memory:4GiB for etcd-heavy labs).
- Provision script runs inside VM as root via `limactl shell $CP_NAME sudo bash /tmp/provision.sh`.
- `etcd-client` (provides etcdctl + etcdutl) installed via `apt install etcd-client` inside provision script.
- Output files produced inside the VM are staged to /tmp/ then copied to host via `limactl copy`.
- fix.sh uses `limactl shell "$CP_NAME" sudo bash -c "..."` for node-level commands.
- cleanup.sh: `limactl delete --force "$CP_NAME" 2>/dev/null || true`.
- Lima labs are excluded from CI (no `.github/workflows/` file).

## kind Lab Pattern
- kind-config.yaml in assets/; extraMounts only when host ? container file sharing is needed.
- `fix.sh` uses `export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"` (not TASK_DIR).
- CI workflow required for all kind labs.

## Naming
- Cluster name: `$EXAM-lab-$LAB_ID` (kind) or `$EXAM-lab-$LAB_ID-cp` / `...-worker` (lima).
- LAB_ID derived from directory name; never hardcode numbers in scripts.

## Idempotency
- fix.sh must be safe to run more than once: use `kubectl apply`, not `kubectl create`.
- etcd snapshot: remove any `.part` file before re-running etcdctl snapshot save.
