# Kubernetes Cluster Upgrade Reference — 4. Upgrade Worker Nodes

> Part of [Kubernetes Cluster Upgrade Reference](../Cluster Upgrade Reference.md)


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

