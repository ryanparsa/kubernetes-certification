## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/secret/

### Create the Secret

```bash
kubectl create secret generic db-secret --from-literal=username=admin --from-literal=password=s3cur3
kubectl get secret db-secret
```

### Pod secret-env -- inject individual keys as env vars

```yaml
# lab/secret-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env
spec:
  containers:
  - name: nginx
    image: nginx
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

```bash
kubectl apply -f lab/secret-env.yaml
kubectl exec secret-env -- printenv DB_USER
kubectl exec secret-env -- printenv DB_PASS
```

Expected: `admin` and `s3cur3`

### Pod secret-vol -- mount entire secret as read-only volume

```yaml
# lab/secret-vol.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-vol
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: secret-mount
      mountPath: /etc/secret
      readOnly: true
  volumes:
  - name: secret-mount
    secret:
      secretName: db-secret
```

```bash
kubectl apply -f lab/secret-vol.yaml
kubectl exec secret-vol -- ls /etc/secret
kubectl exec secret-vol -- cat /etc/secret/username
kubectl exec secret-vol -- cat /etc/secret/password
```

## Checklist (Score: 0/3)

- [ ] Secret `db-secret` exists with keys `username` and `password`
- [ ] Pod `secret-env` has env vars `DB_USER=admin` and `DB_PASS=s3cur3` from secret references
- [ ] Pod `secret-vol` has read-only files `/etc/secret/username` and `/etc/secret/password`
