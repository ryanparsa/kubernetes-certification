## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/#how-pods-manage-multiple-containers

### Create the namespace

```bash
kubectl create namespace multi-container
```

### Create the multi-container pod with shared volume

```yaml
# lab/38.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: multi-container
---
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  namespace: multi-container
spec:
  containers:
  - name: main-container
    image: nginx
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  - name: sidecar-container
    image: busybox
    command: ['sh', '-c', 'while true; do echo $(date) >> /var/log/app.log; sleep 5; done']
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  volumes:
  - name: log-volume
    emptyDir: {}
```

```bash
kubectl apply -f lab/38.yaml
```

### Verify

```bash
kubectl get pod multi-container-pod -n multi-container
kubectl describe pod multi-container-pod -n multi-container | grep -A5 "Containers:"
```

## Checklist (Score: 0/4)

- [ ] Namespace `multi-container` exists
- [ ] Pod `multi-container-pod` exists with two containers
- [ ] Container images are correct (`nginx` and `busybox`)
- [ ] Shared volume `log-volume` is mounted at `/var/log` in both containers
