## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/secret/>

### Create the Secret

```bash
kubectl create secret generic db-secret \
  --from-literal=DB_HOST=db.example.com \
  --from-literal=DB_USER=development \
  --from-literal=DB_PASSWD=password
```

Verify:

```bash
kubectl describe secret db-secret
# Data
# ====
# DB_HOST:    14 bytes
# DB_PASSWD:  8 bytes
# DB_USER:    11 bytes
```

### Pod with envFrom (all keys as env vars)

```yaml
# lab/nginx-secret-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-secret-env
spec:
  containers:
  - image: nginx
    name: nginx-secret-env
    envFrom:
    - secretRef:
        name: db-secret
```

```bash
kubectl apply -f lab/nginx-secret-env.yaml
kubectl exec nginx-secret-env -- env | grep DB_
# DB_HOST=db.example.com
# DB_PASSWD=password
# DB_USER=development
```

### Pod with Secret mounted as a Volume

```yaml
# lab/nginx-secret-vol.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-secret-vol
spec:
  containers:
  - image: nginx
    name: nginx-secret-vol
    volumeMounts:
    - name: db-secret-vol
      mountPath: "/secret"
      readOnly: true
  volumes:
  - name: db-secret-vol
    secret:
      secretName: db-secret
```

```bash
kubectl apply -f lab/nginx-secret-vol.yaml
kubectl exec nginx-secret-vol -- ls /secret
# DB_HOST  DB_PASSWD  DB_USER
kubectl exec nginx-secret-vol -- cat /secret/DB_HOST
# db.example.com
```

## Checklist (Score: 0/6)

- [ ] Secret `db-secret` exists in the `default` namespace
- [ ] Secret contains keys `DB_HOST`, `DB_USER`, `DB_PASSWD` with correct values
- [ ] Pod `nginx-secret-env` uses `envFrom` to inject all Secret keys as env vars
- [ ] Pod `nginx-secret-env` has `DB_HOST` env var set to `db.example.com`
- [ ] Pod `nginx-secret-vol` mounts `db-secret` as a volume at `/secret`
- [ ] `/secret/DB_HOST` inside `nginx-secret-vol` contains `db.example.com`
