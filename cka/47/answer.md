## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

### Create the pod with liveness and readiness probes

```yaml
# lab/health-check.yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
```

```bash
kubectl apply -f lab/health-check.yaml
kubectl wait pod health-check --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod health-check
kubectl describe pod health-check | grep -A5 Liveness
kubectl describe pod health-check | grep -A5 Readiness
```

## Checklist (Score: 0/5)

- [ ] Pod `health-check` exists in namespace `default`
- [ ] Liveness probe uses HTTP GET on path `/` port `80`
- [ ] Liveness probe has `initialDelaySeconds: 5`
- [ ] Readiness probe uses HTTP GET on path `/` port `80`
- [ ] Readiness probe has `initialDelaySeconds: 5`
