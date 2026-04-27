# etcd Reference — 11. HA Clusters and Raft Quorum

> Part of [etcd Reference](../etcd Reference.md)


### Quorum and fault tolerance

| Cluster size | Quorum needed | Max failures tolerated |
|---|---|---|
| 1 | 1 | 0 |
| 3 | 2 | 1 |
| 5 | 3 | 2 |
| 7 | 4 | 3 |

**If quorum is lost**, the cluster enters a **read-only state** — no writes are accepted.
Recovery requires manually starting etcd with `--force-new-cluster` on one node (last resort).

### Checking which node is the leader

```bash
ETCDCTL_API=3 etcdctl endpoint status \
  --endpoints=https://NODE1:2379,https://NODE2:2379,https://NODE3:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --write-out=table
# IS LEADER column shows true on the current leader
```

### Transferring leadership (graceful maintenance)

```bash
# Move the leader away from a node before draining it
etcdctl move-leader <target-member-id>
```

### Defragmenting to reclaim disk space

Over time, deleted keys leave fragmented space in the backend database. Defrag reclaims it:

```bash
# Defrag the local member (run on each member separately, followers first, leader last)
ETCDCTL_API=3 etcdctl defrag \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Check DB size before and after
etcdctl endpoint status --write-out=table
```

---

