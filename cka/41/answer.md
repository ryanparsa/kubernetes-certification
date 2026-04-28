## Answer

**Reference:** https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/

### Create the namespace

```bash
kubectl create namespace monitoring
```

### Create the multi-container pod

```yaml
# lab/logger.yaml
apiVersion: v1
kind: Pod
metadata:
  name: logger
  namespace: monitoring
spec:
  containers:
  - name: busybox
    image: busybox
    command: ['/bin/sh', '-c']
    args:
    - while true; do
        echo "$(date) - Application log entry" >> /var/log/app.log;
        sleep 10;
      done
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  - name: fluentd
    image: fluentd
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  volumes:
  - name: log-volume
    emptyDir: {}
```

```bash
kubectl apply -f lab/logger.yaml
```

### Verify

```bash
kubectl get pod logger -n monitoring
kubectl logs logger -n monitoring -c busybox
```

## Checklist (Score: 0/5)

- [ ] Pod `logger` exists in namespace `monitoring`
- [ ] Pod has container `busybox` writing to `/var/log/app.log`
- [ ] Pod has container `fluentd`
- [ ] Both containers mount volume `log-volume` at `/var/log`
- [ ] Both containers are Running
