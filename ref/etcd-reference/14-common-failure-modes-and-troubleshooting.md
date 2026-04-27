# etcd Reference — 13. Common Failure Modes and Troubleshooting

> Part of [etcd Reference](../etcd Reference.md)


### etcd pod not starting

```bash
# Check static pod logs via crictl (API server may not be available)
crictl ps -a | grep etcd
crictl logs <container-id>

# Common causes:
# - Wrong --data-dir path (directory doesn't exist or is empty after a bad restore)
# - Wrong cert paths in the manifest
# - Port 2379/2380 already in use
# - Corrupted WAL in data directory
```

### API server cannot connect to etcd

```bash
# Check API server logs
crictl logs <apiserver-container-id>

# Look for: "connection refused", "certificate signed by unknown authority", "context deadline exceeded"

# Verify etcd is listening
ss -tlnp | grep 2379

# Test connectivity with the exact certs the API server uses
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key
```

### etcd is healthy but cluster state seems wrong / missing objects

```bash
# Check if the data directory was accidentally reset (e.g. after a bad restore)
ls -lah /var/lib/etcd/member/

# Check etcd revision — a sudden drop indicates a restore happened
etcdctl endpoint status --write-out=table
# Compare RAFT INDEX and DB SIZE against expected values
```

### Disk space / database quota exceeded

```bash
# Check backend DB size
etcdctl endpoint status --write-out=table
# If DB SIZE approaches quota-backend-bytes, the cluster becomes read-only

# Compact old revisions (safe to run on leader)
rev=$(etcdctl endpoint status --write-out=json | jq '.[0].Status.header.revision')
etcdctl compact $rev

# Defrag after compaction
etcdctl defrag

# Increase quota (edit etcd.yaml)
# --quota-backend-bytes=8589934592   # 8 GiB
```

### Troubleshooting certificate issues

```bash
# Inspect a certificate
openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -noout -text | \
  grep -E 'Subject:|Issuer:|Not After|IP Address|DNS'

# Check cert expiry
kubeadm certs check-expiration | grep etcd

# Renew etcd certs
kubeadm certs renew etcd-server
kubeadm certs renew etcd-peer
kubeadm certs renew etcd-healthcheck-client
kubeadm certs renew apiserver-etcd-client
```

---

