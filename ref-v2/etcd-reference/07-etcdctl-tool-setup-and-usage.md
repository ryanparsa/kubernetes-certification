# etcd Reference

[← Back to index](../README.md)

---

## 6. etcdctl — Tool Setup and Usage

`etcdctl` is the CLI client for etcd. Always set `ETCDCTL_API=3` (v2 is deprecated and
uses a different data model).

### Installation (if not available on host)

```bash
# Check if installed
which etcdctl

# If not, find the binary inside the etcd pod and copy it out
kubectl -n kube-system cp \
  etcd-<node>:/usr/local/bin/etcdctl \
  /usr/local/bin/etcdctl
chmod +x /usr/local/bin/etcdctl
```

### Setting environment variables (saves repeating flags)

```bash
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
```

Once set, commands become much shorter:

```bash
etcdctl endpoint health
etcdctl member list
etcdctl snapshot save /tmp/backup.db
```

### Running etcdctl inside the etcd pod

Useful when `etcdctl` is not installed on the host:

```bash
kubectl -n kube-system exec -it etcd-<node> -- sh

# Inside the pod (certs are already mounted):
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health
```

### Output formats

```bash
# Table (human-readable)
etcdctl member list --write-out=table

# JSON (scriptable)
etcdctl endpoint status --write-out=json | jq .

# Simple (key=value)
etcdctl endpoint status --write-out=simple
```

---
