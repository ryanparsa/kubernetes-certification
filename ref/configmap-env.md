# Consuming as Environment Variables

### Individual keys — `valueFrom`

```yaml
spec:
  containers:
  - name: app
    image: my-app:v1
    env:
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: DB_PASSWORD
```

### All keys at once — `envFrom`

```yaml
spec:
  containers:
  - name: app
    image: my-app:v1
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: db-credentials
    - configMapRef:
        name: feature-flags
        optional: true    # don't fail if the ConfigMap doesn't exist
```

> `envFrom` injects every key as an environment variable. Keys that are invalid
> environment variable names (e.g. contain dots) are silently ignored.

---

