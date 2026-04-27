# Secrets

Secrets store sensitive data (passwords, tokens, certificates). Values are base64-encoded
at rest (not encrypted by default — enable encryption-at-rest separately).

### Create imperatively

```bash
# Generic / Opaque secret from literals
kubectl create secret generic db-credentials \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASSWORD=s3cr3t

# From files
kubectl create secret generic tls-files \
  --from-file=tls.crt \
  --from-file=tls.key

# TLS secret (validates cert/key pair)
kubectl create secret tls my-tls \
  --cert=tls.crt \
  --key=tls.key

# Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=me@example.com
```

### Secret YAML

Values must be **base64-encoded** in the `data` field, or plain text in `stringData`
(Kubernetes encodes `stringData` automatically on write).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: my-app
type: Opaque
data:
  DB_USER: YWRtaW4=          # echo -n 'admin' | base64
  DB_PASSWORD: czNjcjN0       # echo -n 's3cr3t' | base64
```

```yaml
# Using stringData (plain text — easier for humans)
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: my-app
type: Opaque
stringData:
  DB_USER: admin
  DB_PASSWORD: s3cr3t
```

### Secret types

| Type | Used for |
|---|---|
| `Opaque` | Generic — any key/value data (default) |
| `kubernetes.io/tls` | TLS certificate + private key |
| `kubernetes.io/dockerconfigjson` | Docker registry auth credentials |
| `kubernetes.io/service-account-token` | Service account tokens (legacy) |
| `kubernetes.io/ssh-auth` | SSH private keys |
| `kubernetes.io/basic-auth` | Username and password |

### Immutable Secret

```yaml
apiVersion: v1
kind: Secret
immutable: true
...
```

---

