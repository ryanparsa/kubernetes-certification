# etcd Reference — 8. Inspecting Keys (Reading Cluster State)

> Part of [etcd Reference](../etcd Reference.md)


etcd stores Kubernetes objects under the prefix `/registry/`.

```bash
# List all top-level key prefixes
ETCDCTL_API=3 etcdctl get / --prefix --keys-only \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# List all pods in the default namespace
etcdctl get /registry/pods/default --prefix --keys-only

# Read a specific key (value is protobuf-encoded — use apiserver for human-readable output)
etcdctl get /registry/pods/default/my-pod

# Count all keys (cluster size indicator)
etcdctl get / --prefix --keys-only | wc -l

# Watch all changes to a key prefix in real time
etcdctl watch /registry/pods/default --prefix
```

> Keys are stored as protobuf binary blobs. For human-readable output, always use
> `kubectl get ... -o yaml` via the API server rather than reading etcd directly.

---

