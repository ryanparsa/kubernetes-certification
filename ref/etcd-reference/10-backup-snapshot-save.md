# etcd Reference — 9. Backup — Snapshot Save

> Part of [etcd Reference](../etcd Reference.md)


A snapshot is a **consistent, point-in-time copy** of the etcd keyspace. It captures
all keys at the revision at which the snapshot was taken.

### Take a snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Output:
# Snapshot saved at /tmp/etcd-backup.db
```

### Verify the snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | 7d2aa533 |    91824 |       1527 |     3.3 MB |
# +----------+----------+------------+------------+
```

### Copy a snapshot out of the etcd pod

```bash
kubectl -n kube-system exec etcd-<node> -- \
  etcdctl snapshot save /tmp/backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

kubectl -n kube-system cp etcd-<node>:/tmp/backup.db /tmp/etcd-backup.db
```

---

