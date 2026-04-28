## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/configmap/>

### Create the ConfigMap from a file

```bash
echo -e "DB_URL=localhost:3306\nDB_USERNAME=postgres" > lab/config.txt
kubectl create configmap db-config --from-env-file=lab/config.txt
```

### Create the Pod manifest

```bash
kubectl run backend --image=nginx --dry-run=client -o yaml > lab/backend.yaml
```

Edit `lab/backend.yaml` to add `envFrom`:

```yaml
# lab/backend.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: backend
  name: backend
spec:
  containers:
  - image: nginx
    name: backend
    envFrom:
    - configMapRef:
        name: db-config
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
```

```bash
kubectl apply -f lab/backend.yaml
kubectl wait pod/backend --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec backend -- env | grep -E 'DB_URL|DB_USERNAME'
# DB_URL=localhost:3306
# DB_USERNAME=postgres
```

## Checklist (Score: 0/4)

- [ ] ConfigMap `db-config` exists in `default` namespace
- [ ] ConfigMap contains key `DB_URL=localhost:3306`
- [ ] ConfigMap contains key `DB_USERNAME=postgres`
- [ ] Pod `backend` exposes `DB_URL` and `DB_USERNAME` as environment variables
