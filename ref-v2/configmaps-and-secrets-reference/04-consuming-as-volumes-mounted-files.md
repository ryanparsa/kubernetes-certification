# ConfigMaps and Secrets Reference

[← Back to index](../README.md)

---

## 4. Consuming as Volumes (Mounted Files)

Each key in the ConfigMap or Secret becomes a file in the mounted directory.

### ConfigMap volume

```yaml
spec:
  volumes:
  - name: config-vol
    configMap:
      name: app-config
      items:                         # optional: select specific keys
      - key: app.properties
        path: application.properties # filename inside the mount
  containers:
  - name: app
    image: my-app:v1
    volumeMounts:
    - name: config-vol
      mountPath: /etc/config
      readOnly: true
```

### Secret volume

```yaml
spec:
  volumes:
  - name: secret-vol
    secret:
      secretName: db-credentials
      defaultMode: 0400             # restrict file permissions
  containers:
  - name: app
    image: my-app:v1
    volumeMounts:
    - name: secret-vol
      mountPath: /etc/secrets
      readOnly: true
```

Result: `/etc/secrets/DB_USER` and `/etc/secrets/DB_PASSWORD` are created as files
containing the plaintext values (base64-decoded automatically).

---
