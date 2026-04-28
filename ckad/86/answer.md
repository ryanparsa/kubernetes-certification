## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

### Create the namespace

```bash
kubectl create namespace monitoring
```

### Create the Pod with liveness and readiness probes

```yaml
# lab/health-check.yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check
  namespace: monitoring
spec:
  containers:
  - name: nginx
    image: nginx:1.25
    livenessProbe:
      httpGet:
        path: /
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
kubectl apply -f lab/health-check.yaml
kubectl wait pod/health-check -n monitoring --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl describe pod health-check -n monitoring | grep -A 5 "Liveness\|Readiness"
# Expected output shows the HTTP GET probe configuration for both probes
```

## Checklist (Score: 0/3)

- [ ] Pod `health-check` in namespace `monitoring` is Running
- [ ] Liveness probe is HTTP GET `/` on port 80 with `initialDelaySeconds: 10` and `periodSeconds: 5`
- [ ] Readiness probe is HTTP GET `/` on port 80 with `initialDelaySeconds: 5` and `periodSeconds: 3`
