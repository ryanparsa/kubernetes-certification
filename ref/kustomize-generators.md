# Generators

Generators create ConfigMaps or Secrets and automatically append a content hash to
the name (e.g. `app-config-k8d9f2m`). This triggers a rolling update whenever the
data changes.

### ConfigMap generator

```yaml
configMapGenerator:
  - name: app-config
    files:
    - config.properties           # key = filename, value = file contents
    - app.conf=myconfig.conf       # custom key name
    literals:
    - LOG_LEVEL=info
    - MAX_RETRIES=3
    options:
      disableNameSuffixHash: true  # keep original name (no hash)
      labels:
        app: my-app
```

### Secret generator

```yaml
secretGenerator:
  - name: db-credentials
    literals:
    - DB_USER=admin
    - DB_PASSWORD=s3cr3t
    type: Opaque
    options:
      disableNameSuffixHash: true
  - name: tls-secret
    files:
    - tls.crt
    - tls.key
    type: kubernetes.io/tls
```

> When you change a ConfigMap or Secret value, the hash suffix changes, which causes
> the Deployment to see a new volume/env source and roll out automatically.

---

