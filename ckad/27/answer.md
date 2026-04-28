## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

### Create the namespace (if not present)

```bash
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -
```

### Create the pod with health probes

```yaml
# lab/health-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-pod
  namespace: workloads
spec:
  containers:
  - name: whoami
    image: emilevauge/whoami
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 30
      periodSeconds: 15
      timeoutSeconds: 5
      failureThreshold: 3
    readinessProbe:
      tcpSocket:
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 3
```

```bash
kubectl apply -f lab/health-pod.yaml
```

### Verify

```bash
kubectl get pod health-pod -n workloads
kubectl describe pod health-pod -n workloads | grep -A10 "Liveness\|Readiness"
```

## Checklist (Score: 0/3)

- [ ] Pod `health-pod` is running in namespace `workloads`
- [ ] Pod has a liveness probe performing HTTP GET on `/healthz` port `80` every `15` seconds
- [ ] Pod has a readiness probe checking TCP port `80` every `10` seconds
