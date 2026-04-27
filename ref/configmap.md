# ConfigMaps

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

