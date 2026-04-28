## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/configmap/>

### Create the ConfigMap

```bash
kubectl create configmap db-config \
  --from-literal=DB_HOST=db.example.com \
  --from-literal=DB_USER=development \
  --from-literal=DB_PASSWD=password
```

Verify:

```bash
kubectl describe configmap db-config
# Data
# ====
# DB_HOST:    db.example.com
# DB_PASSWD:  password
# DB_USER:    development
```

### Create the Pod

```yaml
# lab/nginx-config.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-config
spec:
  containers:
  - image: nginx
    name: nginx-config
    envFrom:
    - configMapRef:
        name: db-config
    volumeMounts:
    - name: db-config-vol
      mountPath: "/config"
      readOnly: true
  volumes:
  - name: db-config-vol
    configMap:
      name: db-config
```

```bash
kubectl apply -f lab/nginx-config.yaml
```

### Verify

```bash
# Check env vars injected
kubectl exec nginx-config -- env | grep DB_
# DB_HOST=db.example.com
# DB_PASSWD=password
# DB_USER=development

# Check volume mount
kubectl exec nginx-config -- ls /config
# DB_HOST  DB_PASSWD  DB_USER

kubectl exec nginx-config -- cat /config/DB_HOST
# db.example.com
```

## Checklist (Score: 0/6)

- [ ] ConfigMap `db-config` exists in the `default` namespace
- [ ] ConfigMap contains key `DB_HOST=db.example.com`
- [ ] ConfigMap contains key `DB_USER=development`
- [ ] ConfigMap contains key `DB_PASSWD=password`
- [ ] Pod `nginx-config` injects all ConfigMap keys as env vars via `envFrom`
- [ ] Pod `nginx-config` mounts ConfigMap as a volume at `/config`
