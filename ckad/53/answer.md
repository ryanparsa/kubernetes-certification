## Answer

**Reference:** https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/

### Create the namespace

```bash
kubectl create namespace pod-lifecycle
```

### Create the pod with lifecycle hooks

```yaml
# lab/53.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pod-lifecycle
---
apiVersion: v1
kind: Pod
metadata:
  name: lifecycle-pod
  namespace: pod-lifecycle
spec:
  terminationGracePeriodSeconds: 30
  containers:
  - name: nginx
    image: nginx
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo 'Welcome to the pod!' > /usr/share/nginx/html/welcome.txt"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "sleep 10"]
```

```bash
kubectl apply -f lab/53.yaml
kubectl wait pod/lifecycle-pod -n pod-lifecycle --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl describe pod lifecycle-pod -n pod-lifecycle | grep -A10 "PostStart\|PreStop\|Termination"
kubectl exec lifecycle-pod -n pod-lifecycle -- cat /usr/share/nginx/html/welcome.txt
```

## Checklist (Score: 0/5)

- [ ] Namespace `pod-lifecycle` exists
- [ ] Pod `lifecycle-pod` is created with image `nginx`
- [ ] postStart hook creates `/usr/share/nginx/html/welcome.txt` with content `Welcome to the pod!`
- [ ] preStop hook runs `sleep 10`
- [ ] Termination grace period is set to `30` seconds
