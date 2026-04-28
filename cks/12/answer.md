## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/secret/

### Create the namespace

```bash
kubectl create namespace secrets-management
```

### Create the Secret

```bash
kubectl create secret generic db-creds \
  --from-literal=username=admin \
  --from-literal=password='SecretP@ssw0rd' \
  -n secrets-management
```

Or declaratively (values must be base64-encoded):

```yaml
# lab/db-creds.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-creds
  namespace: secrets-management
type: Opaque
stringData:
  username: admin
  password: "SecretP@ssw0rd"
```

```bash
kubectl apply -f lab/db-creds.yaml
```

### Create the pod that mounts the secret as files

```yaml
# lab/secure-app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: secrets-management
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/db-creds
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-creds
```

```bash
kubectl apply -f lab/secure-app.yaml
kubectl wait pod secure-app -n secrets-management --for=condition=Ready --timeout=60s
```

### Create the pod that exposes the secret as environment variables

```yaml
# lab/env-app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-app
  namespace: secrets-management
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: username
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: password
```

```bash
kubectl apply -f lab/env-app.yaml
kubectl wait pod env-app -n secrets-management --for=condition=Ready --timeout=60s
```

### Verify

```bash
# Check secret exists
kubectl get secret db-creds -n secrets-management

# Check file mount
kubectl exec secure-app -n secrets-management -- ls /etc/db-creds
kubectl exec secure-app -n secrets-management -- cat /etc/db-creds/username

# Check env vars
kubectl exec env-app -n secrets-management -- env | grep DB_
```

> [!NOTE]
> Volume mounts are preferred over environment variables for secrets because env vars are exposed in process listings and child processes, whereas mounted files can be managed with stricter filesystem permissions.

## Checklist (Score: 0/5)

- [ ] Secret `db-creds` exists in namespace `secrets-management` with keys `username` and `password`
- [ ] Pod `secure-app` exists and mounts secret `db-creds` at `/etc/db-creds`
- [ ] Secret files are accessible at `/etc/db-creds/username` and `/etc/db-creds/password`
- [ ] Pod `env-app` exists and exposes secret as env vars `DB_USER` and `DB_PASS`
- [ ] Both pods use `busybox` image and run `sleep 3600`
