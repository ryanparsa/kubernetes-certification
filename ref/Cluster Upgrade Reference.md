# Kubernetes Cluster Upgrade Reference

Reference for upgrading a kubeadm-managed cluster: control-plane node first, then
worker nodes. Covers pre-flight checks, draining, and post-upgrade validation.

---

## 1. Upgrade Overview

Kubernetes supports upgrading **one minor version at a time** (e.g. 1.29 → 1.30).
Skipping minor versions is not supported.

```
1. Upgrade kubeadm on the control-plane node
2. Run kubeadm upgrade plan   → review what will change
3. Run kubeadm upgrade apply  → upgrade control-plane components
4. Upgrade kubelet + kubectl on the control-plane node
5. Repeat steps 1, 3–4 on each additional control-plane node (HA clusters)
6. For each worker node: drain → upgrade kubeadm/kubelet/kubectl → uncordon
```

---

## 2. Pre-flight Checks

```bash
# Check current versions
kubectl version --short
kubeadm version
kubelet --version

# Verify all nodes are Ready before starting
kubectl get nodes

# Confirm which version you can upgrade to
apt-cache madison kubeadm          # Debian/Ubuntu
yum list --showduplicates kubeadm  # RHEL/CentOS
```

---

## 3. Upgrade the Control-Plane Node

### Step 1 — Upgrade kubeadm

```bash
# Debian/Ubuntu
apt-mark unhold kubeadm
apt-get update
apt-get install -y kubeadm=1.30.0-1.1    # use exact target version
apt-mark hold kubeadm

# Verify
kubeadm version
```

### Step 2 — Plan the upgrade

```bash
kubeadm upgrade plan
# Output shows:
#  - Current versions of each component
#  - Target versions available
#  - API Server, Controller Manager, Scheduler, etcd, CoreDNS, kube-proxy versions
```

### Step 3 — Apply the upgrade

```bash
# Upgrade to the specific version shown in the plan
kubeadm upgrade apply v1.30.0

# For additional control-plane nodes (HA only), use:
kubeadm upgrade node
```

### Step 4 — Drain the control-plane node

```bash
# Evict workloads (DaemonSet pods are left in place)
kubectl drain <control-plane-node> \
  --ignore-daemonsets \
  --delete-emptydir-data
```

### Step 5 — Upgrade kubelet and kubectl

```bash
# Debian/Ubuntu
apt-mark unhold kubelet kubectl
apt-get install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
apt-mark hold kubelet kubectl

# Reload and restart kubelet
systemctl daemon-reload
systemctl restart kubelet
```

### Step 6 — Uncordon the control-plane node

```bash
kubectl uncordon <control-plane-node>

# Verify the node is Ready and shows the new version
kubectl get nodes
```

---

## 4. Upgrade Worker Nodes

Repeat these steps for **each worker node** one at a time.

### Step 1 — Drain the worker node (from any node with kubectl access)

```bash
kubectl drain <worker-node> \
  --ignore-daemonsets \
  --delete-emptydir-data
```

### Step 2 — SSH to the worker node and upgrade kubeadm

```bash
ssh <worker-node>

# Debian/Ubuntu
apt-mark unhold kubeadm
apt-get update
apt-get install -y kubeadm=1.30.0-1.1
apt-mark hold kubeadm
```

### Step 3 — Upgrade the node configuration

```bash
# This upgrades the local kubelet config managed by kubeadm
kubeadm upgrade node
```

### Step 4 — Upgrade kubelet and kubectl

```bash
apt-mark unhold kubelet kubectl
apt-get install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
apt-mark hold kubelet kubectl

systemctl daemon-reload
systemctl restart kubelet
```

### Step 5 — Uncordon the worker node (from the control-plane / kubectl)

```bash
kubectl uncordon <worker-node>
```

---

## 5. Post-Upgrade Validation

```bash
# All nodes should show the new version and be Ready
kubectl get nodes
# NAME              STATUS   ROLES           AGE   VERSION
# control-plane     Ready    control-plane   10d   v1.30.0
# worker-1          Ready    <none>          10d   v1.30.0

# Verify system pods are running
kubectl -n kube-system get pods

# Check component versions
kubectl version --short

# Run a quick smoke test
kubectl run smoke --image=nginx --restart=Never
kubectl get pod smoke
kubectl delete pod smoke
```

---

## 6. Reference — Version Skew Policy

| Component | Allowed skew from API server version |
|---|---|
| kubelet | Up to 3 minor versions behind API server |
| kubectl | ±1 minor version from API server |
| kube-controller-manager, kube-scheduler | Must not be newer than API server |
| kubeadm | Same minor version as the target Kubernetes version |

> **Rule of thumb:** upgrade the control-plane first, then workers. Never run a worker
> kubelet on a *newer* version than the API server.

---

## 7. Useful Commands

```bash
# List available kubeadm versions (Debian/Ubuntu)
apt-cache madison kubeadm | head -20

# Hold all Kubernetes packages (prevent accidental upgrades)
apt-mark hold kubeadm kubelet kubectl

# Unhold before intentional upgrade
apt-mark unhold kubeadm kubelet kubectl

# Check kubelet service status after upgrade
systemctl status kubelet

# Watch all nodes come back Ready after upgrade
kubectl get nodes -w
```
