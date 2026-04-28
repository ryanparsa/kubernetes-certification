## Answer

**Reference:** <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>

### Readiness Probe Pod

```yaml
# lab/nginx-readiness.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-readiness
spec:
  containers:
  - image: nginx
    name: nginx-readiness
    readinessProbe:
      httpGet:
        path: /
        port: 80
```

```bash
kubectl apply -f lab/nginx-readiness.yaml
kubectl get pod nginx-readiness
# NAME              READY   STATUS    RESTARTS   AGE
# nginx-readiness   1/1     Running   0          15s
```

### Liveness Probe Pod

```yaml
# lab/nginx-liveness.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-liveness
spec:
  containers:
  - image: nginx
    name: nginx-liveness
    livenessProbe:
      exec:
        command:
        - ls
      initialDelaySeconds: 30
      periodSeconds: 5
```

```bash
kubectl apply -f lab/nginx-liveness.yaml
kubectl get pod nginx-liveness
# NAME             READY   STATUS    RESTARTS   AGE
# nginx-liveness   1/1     Running   0          35s
```

### Verify probe configuration

```bash
kubectl describe pod nginx-readiness | grep -A5 "Readiness:"
# Readiness:  http-get http://:80/ delay=0s timeout=1s period=10s #success=1 #failure=3

kubectl describe pod nginx-liveness | grep -A5 "Liveness:"
# Liveness:   exec [ls] delay=30s timeout=1s period=5s #success=1 #failure=3
```

## Checklist (Score: 0/5)

- [ ] Pod `nginx-readiness` is running
- [ ] `nginx-readiness` has an HTTP GET readiness probe on path `/` port `80`
- [ ] Pod `nginx-liveness` is running
- [ ] `nginx-liveness` has an exec liveness probe running command `ls`
- [ ] `nginx-liveness` liveness probe has `initialDelaySeconds: 30` and `periodSeconds: 5`
