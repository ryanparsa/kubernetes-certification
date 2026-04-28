## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/#using-pods

### Create the multi-container pod

```yaml
# lab/sidecar-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: sidecar-pod
  namespace: troubleshooting
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: log-volume
      mountPath: /var/my-log
  - name: sidecar
    image: busybox
    command: ["sh", "-c", "while true; do date >> /var/my-log/date.log; sleep 10; done"]
    volumeMounts:
    - name: log-volume
      mountPath: /var/my-log
  volumes:
  - name: log-volume
    emptyDir: {}
```

```bash
kubectl apply -f lab/sidecar-pod.yaml
```

### Verify

```bash
kubectl get pod sidecar-pod -n troubleshooting
kubectl exec -it sidecar-pod -n troubleshooting -c nginx -- cat /var/my-log/date.log
```

## Checklist (Score: 0/2)

- [ ] Pod `sidecar-pod` exists in namespace `troubleshooting` with two containers (`nginx` and `sidecar`)
- [ ] Both containers mount the shared volume `log-volume` at `/var/my-log`
