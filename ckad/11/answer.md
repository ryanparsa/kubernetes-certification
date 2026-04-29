## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

### Create probe-pod with liveness and readiness probes

```yaml
# lab/probe-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: probe-pod
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
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
      periodSeconds: 5
```

```bash
kubectl apply -f lab/probe-pod.yaml
kubectl get pod probe-pod
kubectl describe pod probe-pod | grep -A10 "Liveness\|Readiness"
```

### Create broken pod and investigate

```yaml
# lab/broken.yaml
apiVersion: v1
kind: Pod
metadata:
  name: broken
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["ls", "/notexist"]
```

```bash
kubectl apply -f lab/broken.yaml

# Check logs -- will show the error from the command
kubectl logs broken

# Check events and status
kubectl describe pod broken
```

**Expected observations:**

- `kubectl logs broken` shows: `ls: /notexist: No such file or directory`
- `kubectl describe pod broken` shows container exited with non-zero exit code
- Pod status will be `Error` or `CrashLoopBackOff` (if `restartPolicy: Always`)

### Verify probe-pod probes

```bash
kubectl get pod probe-pod -o jsonpath='{.spec.containers[0].livenessProbe}'
kubectl get pod probe-pod -o jsonpath='{.spec.containers[0].readinessProbe}'
```

## Checklist (Score: 0/4)

- [ ] Pod `probe-pod` is running with liveness probe (`httpGet /` port 80, initialDelaySeconds 10, periodSeconds 5)
- [ ] Pod `probe-pod` has readiness probe (`httpGet /` port 80, initialDelaySeconds 5, periodSeconds 5)
- [ ] Pod `broken` created and fails as expected
- [ ] Error identified in logs/events: `ls: /notexist: No such file or directory`
