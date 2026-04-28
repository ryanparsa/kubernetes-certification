## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/secret/>

### Create the Secret

```bash
kubectl create secret generic db-credentials --from-literal=db-password=passwd
kubectl get secrets db-credentials
```

### Create the Pod manifest

```bash
kubectl run backend --image=nginx --dry-run=client -o yaml > lab/backend.yaml
```

Edit `lab/backend.yaml` to inject the secret key as an environment variable:

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
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: db-password
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
kubectl exec backend -- env | grep DB_PASSWORD
# DB_PASSWORD=passwd
```

## Checklist (Score: 0/4)

- [ ] Secret `db-credentials` exists in `default` namespace
- [ ] Secret contains the key `db-password`
- [ ] Pod `backend` is running
- [ ] Pod `backend` exposes `DB_PASSWORD=passwd` as an environment variable
