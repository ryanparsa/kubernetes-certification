# etcd Reference

[← Back to index](../README.md)

---

## 10. Restore — Full Procedure

Restoring from a snapshot **replaces all current cluster state** with the snapshot.

### Single-node restore

#### Step 1 — Stop the API server

```bash
# Prevent writes while etcd is being replaced
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/

# Wait for it to stop (kube-apiserver should disappear from the list)
watch crictl ps
```

#### Step 2 — Restore the snapshot to a new data directory

```bash
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore

# Output:
# {"level":"info","msg":"restoring snapshot","path":"/tmp/etcd-backup.db"}
# {"level":"info","msg":"restored snapshot"}
# {"level":"info","msg":"adding member","member":"..."}
```

> **Do not** restore into `/var/lib/etcd` while etcd is running — always use a new
> directory first, then swap.

#### Step 3 — Point etcd at the new data directory

Edit `/etc/kubernetes/manifests/etcd.yaml` and update **two places**:

```yaml
# 1. The --data-dir flag
- --data-dir=/var/lib/etcd-restore      # was /var/lib/etcd

# 2. The hostPath volume for etcd-data
volumes:
- hostPath:
    path: /var/lib/etcd-restore          # was /var/lib/etcd
    type: DirectoryOrCreate
  name: etcd-data
```

#### Step 4 — Restore the API server

```bash
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
```

#### Step 5 — Verify recovery

```bash
# Watch pods restart
watch crictl ps

# Confirm cluster is functional
kubectl get nodes
kubectl get pods -A
```

---

### HA cluster restore

In an HA cluster each etcd member must be restored independently.

#### Key differences from single-node

- Stop the API server on **all** control-plane nodes first.
- Run `snapshot restore` on **each** member with member-specific flags:

```bash
# Member 1
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore \
  --name=node1 \
  --initial-cluster=node1=https://10.0.0.1:2380,node2=https://10.0.0.2:2380,node3=https://10.0.0.3:2380 \
  --initial-cluster-token=etcd-cluster-restored \
  --initial-advertise-peer-urls=https://10.0.0.1:2380

# Member 2
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore \
  --name=node2 \
  --initial-cluster=node1=https://10.0.0.1:2380,node2=https://10.0.0.2:2380,node3=https://10.0.0.3:2380 \
  --initial-cluster-token=etcd-cluster-restored \
  --initial-advertise-peer-urls=https://10.0.0.2:2380

# Member 3 — same pattern
```

> Use a **new `--initial-cluster-token`** (e.g. append `-restored`) to prevent the
> restored members from accidentally joining the old (corrupted) cluster.

- Update `etcd.yaml` on each control-plane node to use the new `--data-dir`.
- Restore API server manifests on all nodes.

---
