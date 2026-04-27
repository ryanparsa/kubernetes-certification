# etcd Reference

[← Back to index](../README.md)

---

## 12. Encryption at Rest

By default, Secrets stored in etcd are **base64-encoded but not encrypted**. Enable
encryption-at-rest to protect them.

### Create an EncryptionConfiguration

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <32-byte base64-encoded key>   # openssl rand -base64 32
  - identity: {}   # fallback: read unencrypted secrets written before encryption was enabled
```

```bash
# Generate a 32-byte key
openssl rand -base64 32
```

### Enable in kube-apiserver

Add the flag to `/etc/kubernetes/manifests/kube-apiserver.yaml`:

```yaml
- --encryption-provider-config=/etc/kubernetes/encryption-config.yaml
```

Also add a volume mount so the file is accessible inside the static pod:

```yaml
volumeMounts:
- mountPath: /etc/kubernetes/encryption-config.yaml
  name: encryption-config
  readOnly: true
volumes:
- hostPath:
    path: /etc/kubernetes/encryption-config.yaml
    type: File
  name: encryption-config
```

### Encrypt existing secrets

After enabling, newly written Secrets are encrypted. Rotate existing ones:

```bash
# Re-write all Secrets through the API server (forces encryption)
kubectl get secrets -A -o json | kubectl replace -f -
```

### Verify encryption

```bash
# Read the raw etcd value — should be opaque (not human-readable JSON/YAML)
ETCDCTL_API=3 etcdctl get /registry/secrets/default/my-secret \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  | hexdump -C | head

# Encrypted values start with: k8s:enc:aescbc:v1:
```

---
