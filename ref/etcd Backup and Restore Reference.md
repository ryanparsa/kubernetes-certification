# etcd Backup and Restore Reference

> **This file has been superseded.**
> Full coverage of etcd — including architecture, PKI, etcdctl setup, health checks,
> key inspection, backup, restore, HA membership, encryption at rest, and troubleshooting
> — is now in **[etcd Reference.md](etcd%20Reference.md)**.
>
> The content below is kept for reference but the dedicated file is the authoritative source.

---

---

## 1. Key Concepts

- etcd stores **all cluster state**: pods, secrets, configmaps, deployments, RBAC, etc.
- A snapshot is a consistent point-in-time copy of the etcd keyspace.
- Restoring replaces the entire etcd data directory — the cluster reverts to the state
  captured in the snapshot.
- Always use `ETCDCTL_API=3` — the v2 API is deprecated and data-incompatible.

---

## 2. Locating etcd Connection Parameters

The easiest way to find the correct flags is to inspect the etcd static pod:

```bash
kubectl -n kube-system describe pod etcd-<node>
# or
cat /etc/kubernetes/manifests/etcd.yaml
```

Look for these flags:

| Flag | Typical value |
|---|---|
| `--listen-client-urls` | `https://127.0.0.1:2379` |
| `--cert-file` | `/etc/kubernetes/pki/etcd/server.crt` |
| `--key-file` | `/etc/kubernetes/pki/etcd/server.key` |
| `--trusted-ca-file` | `/etc/kubernetes/pki/etcd/ca.crt` |
| `--data-dir` | `/var/lib/etcd` |

---

## 3. Taking a Snapshot (Backup)

```bash
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Expected output:
# Snapshot saved at /tmp/etcd-backup.db
```

### Verify the snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db \
  --write-out=table

# Output:
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | abc12345 |    87234 |       1423 |     3.1 MB |
# +----------+----------+------------+------------+
```

---

## 4. Restoring from a Snapshot

### Step 1 — Stop the API server (prevents writes during restore)

```bash
# Move the kube-apiserver static pod manifest out of the watched directory
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/

# Wait for the API server to stop
watch crictl ps   # wait until kube-apiserver disappears
```

### Step 2 — Restore the snapshot to a new data directory

```bash
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Output:
# {"level":"info","msg":"restoring snapshot","path":"/tmp/etcd-backup.db"}
# {"level":"info","msg":"restored snapshot"}
```

> The restore command creates a **new** data directory (`/var/lib/etcd-restore`).
> Do **not** restore into the live data directory (`/var/lib/etcd`) while etcd is running.

### Step 3 — Update etcd to use the restored data directory

```bash
vim /etc/kubernetes/manifests/etcd.yaml
```

Find the `--data-dir` flag and the `hostPath` volume mount, and update both:

```yaml
# Before:
- --data-dir=/var/lib/etcd

# After:
- --data-dir=/var/lib/etcd-restore
```

Also update the `volumes` section:

```yaml
volumes:
- hostPath:
    path: /var/lib/etcd-restore   # was /var/lib/etcd
    type: DirectoryOrCreate
  name: etcd-data
```

### Step 4 — Restore the API server manifest

```bash
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
```

### Step 5 — Wait for recovery

```bash
# Watch for the control-plane pods to come back
watch crictl ps

# Once up, verify cluster state is restored
kubectl get pods -A
kubectl get nodes
```

---

## 5. Running etcdctl Inside the etcd Pod

If `etcdctl` is not installed on the host, run it directly inside the etcd container:

```bash
# Find the etcd container ID
crictl ps | grep etcd

# Exec in
kubectl -n kube-system exec -it etcd-<node> -- sh

# Inside the pod — all flags are identical
ETCDCTL_API=3 etcdctl snapshot save /tmp/backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Copy the snapshot out of the pod
kubectl -n kube-system cp etcd-<node>:/tmp/backup.db /tmp/etcd-backup.db
```

---

## 6. HA Cluster Considerations

In an HA cluster (3 or 5 etcd members), each member has its own data directory.

```bash
# List all etcd members
ETCDCTL_API=3 etcdctl member list \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Check health of all members
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://MEMBER1:2379,https://MEMBER2:2379,https://MEMBER3:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

For a full HA restore:
1. Stop the API server on **all** control-plane nodes.
2. Restore the snapshot on **each** etcd member, using a **unique** `--initial-cluster-token` and the correct `--name` and `--initial-advertise-peer-urls` per member.
3. Update `--data-dir` in `etcd.yaml` on each node.
4. Restart API servers.

---

## 7. Quick Reference

```bash
# Backup (one-liner)
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore to new data dir
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore

# Check cluster is healthy after restore
kubectl get nodes
kubectl -n kube-system get pods
```

| Step | Command / action |
|---|---|
| Save snapshot | `etcdctl snapshot save <path>` |
| Verify snapshot | `etcdctl snapshot status <path> --write-out=table` |
| Restore snapshot | `etcdctl snapshot restore <path> --data-dir=<new-dir>` |
| Update data dir | Edit `etcd.yaml` `--data-dir` and `hostPath.path` |
| Restart API server | Move `kube-apiserver.yaml` back to `manifests/` |
