# etcd Reference

[← Back to index](../README.md)

---

## 7. Health Checks and Member Operations

### Single-node health

```bash
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Healthy output:
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.3ms
```

### Endpoint status (shows leader, Raft index, DB size)

```bash
ETCDCTL_API=3 etcdctl endpoint status \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --write-out=table

# +------------------------+------------------+---------+---------+-----------+
# |        ENDPOINT        |        ID        | VERSION | DB SIZE | IS LEADER |
# +------------------------+------------------+---------+---------+-----------+
# | https://127.0.0.1:2379 | 8e9e05c52164694d |  3.5.11 |  3.1 MB |      true |
# +------------------------+------------------+---------+---------+-----------+
```

### Member list (HA clusters)

```bash
ETCDCTL_API=3 etcdctl member list \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --write-out=table

# +------------------+---------+-------+--------------------------+--------------------------+
# |        ID        | STATUS  | NAME  |       PEER ADDRS         |      CLIENT ADDRS        |
# +------------------+---------+-------+--------------------------+--------------------------+
# | 8e9e05c52164694d | started | node1 | https://10.0.0.1:2380    | https://10.0.0.1:2379    |
# | 9cf75dc4f1b0bd57 | started | node2 | https://10.0.0.2:2380    | https://10.0.0.2:2379    |
# | ede3c83b6e348b58 | started | node3 | https://10.0.0.3:2380    | https://10.0.0.3:2379    |
# +------------------+---------+-------+--------------------------+--------------------------+
```

### Add / remove a member (HA maintenance)

```bash
# Add a new member (run before starting etcd on the new node)
etcdctl member add node4 --peer-urls=https://10.0.0.4:2380

# Remove a failed member (use the member ID from member list)
etcdctl member remove 9cf75dc4f1b0bd57

# Update peer URL of an existing member
etcdctl member update 8e9e05c52164694d --peer-urls=https://10.0.0.10:2380
```

---
