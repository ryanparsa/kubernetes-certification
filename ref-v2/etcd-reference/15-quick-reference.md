# etcd Reference

[← Back to index](../README.md)

---

## 14. Quick Reference

### etcdctl flags cheatsheet

| Flag | Purpose |
|---|---|
| `--endpoints` | Comma-separated list of etcd client URLs |
| `--cacert` | Path to etcd CA cert (`etcd/ca.crt`) |
| `--cert` | Path to client cert (server cert or healthcheck-client cert) |
| `--key` | Path to client private key |
| `--write-out` | Output format: `table`, `json`, `simple` |

### Common commands

```bash
# Health check
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Endpoint status (leader, DB size, Raft index)
ETCDCTL_API=3 etcdctl endpoint status --write-out=table \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Member list
ETCDCTL_API=3 etcdctl member list --write-out=table \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Backup
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore

# Check cert expiry
kubeadm certs check-expiration | grep etcd
```

### Restore procedure summary

| Step | Action |
|---|---|
| 1 | `mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/` |
| 2 | `etcdctl snapshot restore <file> --data-dir=<new-dir>` |
| 3 | Edit `etcd.yaml`: update `--data-dir` and `hostPath.path` |
| 4 | `mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/` |
| 5 | `watch crictl ps` → confirm pods come back |
| 6 | `kubectl get nodes && kubectl get pods -A` |
