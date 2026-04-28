## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/secret/

### Create the namespace (if not present)

```bash
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -
```

### Create the Secret

```bash
kubectl create secret generic db-credentials -n workloads \
  --from-literal=username=admin \
  --from-literal=password=securepass \
  --from-literal=random=true
```

### Create the pod with Secret environment variables

```yaml
# lab/secure-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
  namespace: workloads
spec:
  containers:
  - name: mysql
    image: mysql:9.5.0
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
    - name: MYSQL_RANDOM_ROOT_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: random
  restartPolicy: Always
```

```bash
kubectl apply -f lab/secure-pod.yaml
```

### Verify

```bash
kubectl get pod secure-pod -n workloads
kubectl get secret db-credentials -n workloads
```

## Checklist (Score: 0/3)

- [ ] Secret `db-credentials` exists in namespace `workloads` with keys `username`, `password`, and `random`
- [ ] Pod `secure-pod` is running in namespace `workloads`
- [ ] Pod environment variables `DB_USER`, `DB_PASSWORD`, and `MYSQL_RANDOM_ROOT_PASSWORD` are sourced from Secret `db-credentials`
