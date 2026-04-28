## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

### Create the namespace

```bash
kubectl create namespace health-checks
```

### Create the pod with all three probes

```yaml
# lab/52.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: health-checks
---
apiVersion: v1
kind: Pod
metadata:
  name: health-check-pod
  namespace: health-checks
spec:
  containers:
  - name: nginx
    image: nginx
    startupProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 3
      failureThreshold: 3
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 15
      periodSeconds: 5
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 3
      failureThreshold: 3
```

```bash
kubectl apply -f lab/52.yaml
kubectl wait pod/health-check-pod -n health-checks --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl describe pod health-check-pod -n health-checks | grep -A10 "Startup\|Liveness\|Readiness"
```

## Checklist (Score: 0/5)

- [ ] Namespace `health-checks` exists
- [ ] Pod `health-check-pod` is created with image `nginx`
- [ ] Startup probe is configured (HTTP GET port `80`, delay `10s`, period `3s`, failureThreshold `3`)
- [ ] Liveness probe is configured (HTTP GET port `80`, delay `15s`, period `5s`, failureThreshold `3`)
- [ ] Readiness probe is configured (HTTP GET port `80`, delay `5s`, period `3s`, failureThreshold `3`)
