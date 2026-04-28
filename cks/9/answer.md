## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

### Create the namespace

```bash
kubectl create namespace os-hardening
```

### Create the pod with minimal security context

nginx needs writable directories for cache, run, and tmp even when the root filesystem is read-only. Use `emptyDir` volumes for those paths.

```yaml
# lab/secure-container.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-container
  namespace: os-hardening
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
    securityContext:
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
      readOnlyRootFilesystem: true
      runAsUser: 1000
      runAsGroup: 3000
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: var-cache-nginx
      mountPath: /var/cache/nginx
    - name: var-run
      mountPath: /var/run
  volumes:
  - name: tmp
    emptyDir: {}
  - name: var-cache-nginx
    emptyDir: {}
  - name: var-run
    emptyDir: {}
```

```bash
kubectl apply -f lab/secure-container.yaml
kubectl wait pod secure-container -n os-hardening --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod secure-container -n os-hardening
kubectl get pod secure-container -n os-hardening -o jsonpath='{.spec.containers[0].securityContext}'
```

## Checklist (Score: 0/5)

- [ ] Pod `secure-container` exists in namespace `os-hardening`
- [ ] Container drops ALL capabilities and adds back `NET_BIND_SERVICE`
- [ ] Container uses `readOnlyRootFilesystem: true`
- [ ] Container runs as user ID 1000 (`runAsUser: 1000`)
- [ ] Container runs as group ID 3000 (`runAsGroup: 3000`)
