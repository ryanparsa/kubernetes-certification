# etcd Health Check

```bash
# Find etcd pod and its certificates
kubectl -n kube-system describe pod etcd-<node>
# Look for: --cert-file, --key-file, --trusted-ca-file, --listen-client-urls

# Run etcdctl inside the etcd pod
kubectl -n kube-system exec -it etcd-<node> -- sh

# Inside etcd pod (or with ETCDCTL_API=3 set):
etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health

# Output when healthy:
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.3ms

# Check cluster membership (HA clusters)
etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  member list

# Quick backup
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /tmp/etcd-backup.db

# Verify backup
etcdctl snapshot status /tmp/etcd-backup.db --write-out=table
```

---

