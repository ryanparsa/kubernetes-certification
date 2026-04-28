## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod

### Create the namespace

```bash
kubectl create namespace secrets-ns
```

### Create the Secret

```bash
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=SuperSecret123 \
  -n secrets-ns
```

### Create the Pod with Secret volume mount

```yaml
# lab/secret-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
  namespace: secrets-ns
spec:
  containers:
  - name: app
    image: alpine
    command: ["sleep", "3600"]
    volumeMounts:
    - name: secret-vol
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-vol
    secret:
      secretName: db-secret
```

```bash
kubectl apply -f lab/secret-pod.yaml
kubectl wait pod/secret-pod -n secrets-ns --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec secret-pod -n secrets-ns -- ls /etc/secrets/
# Output: password  username
kubectl exec secret-pod -n secrets-ns -- cat /etc/secrets/username
# Output: admin
```

## Checklist (Score: 0/3)

- [ ] Secret `db-secret` exists in namespace `secrets-ns` with keys `username` and `password`
- [ ] Pod `secret-pod` in namespace `secrets-ns` is Running
- [ ] Secret is mounted as a volume at `/etc/secrets` inside the container
