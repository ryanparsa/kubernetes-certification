# etcd Reference

[← Back to index](../README.md)

---

## 3. How etcd Runs in Kubernetes

In a kubeadm cluster, etcd runs as a **static pod** on the control-plane node(s),
managed directly by kubelet from the manifest at:

```
/etc/kubernetes/manifests/etcd.yaml
```

### Key ports

| Port | Protocol | Purpose |
|---|---|---|
| `2379` | HTTPS | Client API — used by kube-apiserver to read/write data |
| `2380` | HTTPS | Peer API — used for Raft replication between etcd members (HA only) |

### Data directory

```
/var/lib/etcd/       ← default data directory; contains the Raft WAL and snapshots
```

---
