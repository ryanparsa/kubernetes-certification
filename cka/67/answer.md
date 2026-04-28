## Answer

**Reference:** https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/

### Investigate the failing deployment

```bash
kubectl get deployment failing-app -n troubleshoot
kubectl describe deployment failing-app -n troubleshoot
kubectl get pods -n troubleshoot
kubectl describe pod <pod-name> -n troubleshoot
kubectl logs <pod-name> -n troubleshoot
```

### Fix all three issues

The deployment has three problems that need to be corrected:

1. Container port should be `80`, not `8080`
2. Memory limit should be `256Mi`, not `64Mi`
3. Liveness probe should check port `80`, not `8080`

```bash
kubectl edit deployment failing-app -n troubleshoot
```

Or apply the fixed manifest directly:

```yaml
# lab/67-fix.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: failing-app
  namespace: troubleshoot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: failing-app
  template:
    metadata:
      labels:
        app: failing-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 10
```

```bash
kubectl apply -f lab/67-fix.yaml
kubectl rollout status deployment/failing-app -n troubleshoot
kubectl wait deployment failing-app -n troubleshoot --for=condition=Available --timeout=120s
```

### Verify

```bash
kubectl get pods -n troubleshoot
# All 3 pods should be Running and Ready
kubectl describe deployment failing-app -n troubleshoot | grep -A5 "Containers:"
```

## Checklist (Score: 0/5)

- [ ] Deployment `failing-app` exists in `troubleshoot` namespace with `3` replicas
- [ ] Container port is corrected to `80`
- [ ] Memory limit is corrected to `256Mi`
- [ ] Liveness probe checks port `80` (not `8080`)
- [ ] All 3 pods are `Running` and `Ready`
