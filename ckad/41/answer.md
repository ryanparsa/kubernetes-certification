## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

### Create the *Namespace*

```bash
kubectl create namespace observability
```

### Create the *Pod* with probes and resource limits

```yaml
# lab/41.yaml
apiVersion: v1
kind: Pod
metadata:
  name: probes-pod
  namespace: observability
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 5
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 3
```

```bash
kubectl apply -f lab/41.yaml
kubectl wait pod/probes-pod -n observability --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl describe pod probes-pod -n observability | grep -A8 "Liveness\|Readiness\|Limits\|Requests"
```

## Checklist (Score: 0/5)

- [ ] *Namespace* `observability` exists
- [ ] *Pod* `probes-pod` is created with image `nginx`
- [ ] Liveness probe is configured correctly (path `/healthz`, port `80`, delay `10s`, period `5s`)
- [ ] Readiness probe is configured correctly (path `/`, port `80`, delay `5s`, period `3s`)
- [ ] Resource requests (`100m` CPU, `128Mi` memory) and limits (`200m` CPU, `256Mi` memory) are set
