# etcd Reference

[← Back to index](../README.md)

---

## 5. etcd PKI / TLS

etcd uses its **own, independent CA** (`/etc/kubernetes/pki/etcd/ca.crt`) separate from
the main cluster CA. Even if the cluster CA were compromised, an attacker still could
not connect to etcd directly.

### Certificate files

| File | Holder | Purpose |
|---|---|---|
| `etcd/ca.crt` | Everyone | Root CA that signs all etcd certs |
| `etcd/ca.key` | etcd CA process | Signs new etcd certs (protect carefully) |
| `etcd/server.crt / server.key` | etcd server | Presented to kube-apiserver (TLS server cert) |
| `etcd/peer.crt / peer.key` | etcd nodes | Mutual TLS between etcd members in HA clusters |
| `etcd/healthcheck-client.crt / key` | etcd liveness probe | Minimal access: health endpoint only |
| `apiserver-etcd-client.crt / key` | kube-apiserver | Client cert apiserver uses to authenticate to etcd |

### Communication diagram

```
kube-apiserver
  → presents apiserver-etcd-client.crt (signed by etcd CA)
  → connects to etcd server.crt:2379
  → etcd verifies: cert signed by etcd/ca.crt ✓

etcd-node-1 (HA)
  → presents peer.crt (signed by etcd CA)
  → connects to etcd-node-2:2380
  → etcd-node-2 verifies: cert signed by etcd/ca.crt ✓
```

### Finding cert paths from the running pod

```bash
kubectl -n kube-system describe pod etcd-<node> | grep "\-\-cert\|\-\-key\|\-\-ca"
# or
grep -E 'cert|key|ca' /etc/kubernetes/manifests/etcd.yaml
```

---
