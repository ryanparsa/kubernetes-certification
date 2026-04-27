# Kubernetes Cluster Upgrade Reference — 3. Upgrade the Control-Plane Node

> Part of [Kubernetes Cluster Upgrade Reference](../Cluster Upgrade Reference.md)


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

