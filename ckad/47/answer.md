## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

### Create the namespace

```bash
kubectl create namespace security
```

### Create the secure pod

```yaml
# lab/47.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: security
---
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: security
spec:
  securityContext:
    runAsUser: 1000
    runAsNonRoot: true
  containers:
  - name: nginx
    image: nginx:alpine
    securityContext:
      capabilities:
        drop: ["ALL"]
      readOnlyRootFilesystem: true
      runAsNonRoot: true
```

```bash
kubectl apply -f lab/47.yaml
kubectl wait pod/secure-app -n security --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod secure-app -n security
kubectl describe pod secure-app -n security | grep -A10 "Security Context"
```

## Checklist (Score: 0/4)

- [ ] Namespace `security` exists
- [ ] Pod `secure-app` is created with image `nginx:alpine`
- [ ] Pod runs as non-root user (UID `1000`)
- [ ] Container security context drops all capabilities and sets `readOnlyRootFilesystem=true`
