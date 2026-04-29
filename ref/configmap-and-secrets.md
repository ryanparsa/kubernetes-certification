# ConfigMaps and Secrets Reference

Reference for creating, mounting, and consuming ConfigMaps and Secrets in Kubernetes.
Covers imperative commands, YAML definitions, environment variable injection, volume
mounts, and common Secret types.

---

## 1. ConfigMaps

A ConfigMap stores non-sensitive key/value configuration data that pods can consume
as environment variables or mounted files.

### Create imperatively

```bash
# From literal key/value pairs
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=info \
  --from-literal=MAX_RETRIES=3

# From a file (key = filename, value = file contents)
kubectl create configmap app-config --from-file=app.properties

# From a file with a custom key name
kubectl create configmap app-config --from-file=config=app.properties

# From an entire directory (one key per file)
kubectl create configmap app-config --from-file=./config-dir/

# Dry-run to generate YAML
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=info \
  --dry-run=client -o yaml
```

### ConfigMap YAML

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: my-app
data:
  LOG_LEVEL: info
  MAX_RETRIES: "3"
  app.properties: |
    server.port=8080
    spring.datasource.url=jdbc:postgresql://db:5432/mydb
```

### Immutable ConfigMap (Kubernetes 1.21+)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
immutable: true   # prevents changes; must delete and re-create to update
data:
  VERSION: "1.0.0"
```

---

## 2. Secrets

Secrets store sensitive data (passwords, tokens, certificates). Values are base64-encoded
at rest (not encrypted by default - enable encryption-at-rest separately).

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
# Using stringData (plain text - easier for humans)
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
| `Opaque` | Generic - any key/value data (default) |
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

## 3. Consuming as Environment Variables

### Individual keys - `valueFrom`

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

### All keys at once - `envFrom`

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

## 5. TLS Secret in an Ingress

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: my-app
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded cert>
  tls.key: <base64-encoded key>
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: my-app
spec:
  tls:
  - hosts:
    - app.example.com
    secretName: tls-secret
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

---

## 6. Useful Commands

```bash
# List ConfigMaps
kubectl get configmap -n my-app

# Describe a ConfigMap (see keys, not values)
kubectl describe configmap app-config -n my-app

# View ConfigMap data
kubectl get configmap app-config -n my-app -o yaml

# Edit a ConfigMap in-place
kubectl edit configmap app-config -n my-app

# List Secrets (values are hidden)
kubectl get secret -n my-app

# Describe a Secret (shows types and data keys, NOT values)
kubectl describe secret db-credentials -n my-app

# Decode a Secret value
kubectl get secret db-credentials -n my-app \
  -o jsonpath='{.data.DB_PASSWORD}' | base64 --decode

# Delete a ConfigMap or Secret
kubectl delete configmap app-config -n my-app
kubectl delete secret db-credentials -n my-app
```

---

## 7. Quick Reference

| Task | ConfigMap | Secret |
|---|---|---|
| Create from literals | `kubectl create configmap cm --from-literal=k=v` | `kubectl create secret generic s --from-literal=k=v` |
| Create from file | `kubectl create configmap cm --from-file=file` | `kubectl create secret generic s --from-file=file` |
| Inject all keys as env vars | `envFrom.configMapRef` | `envFrom.secretRef` |
| Inject single key as env var | `env[].valueFrom.configMapKeyRef` | `env[].valueFrom.secretKeyRef` |
| Mount as files | `volumes[].configMap` | `volumes[].secret` |
| Decode value | - | `kubectl get secret ... -o jsonpath='{.data.KEY}' \| base64 --decode` |

> **Important:** Pods do **not** automatically pick up ConfigMap or Secret changes
> when using `envFrom`/`env`. The pod must be restarted. Volume-mounted files update
> automatically (with a short kubelet sync delay).
