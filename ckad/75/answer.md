## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/pods/#how-pods-manage-multiple-containers>

### Create the Pod manifest

```yaml
# lab/adapter.yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter
spec:
  volumes:
  - name: log-vol
    emptyDir: {}
  containers:
  - name: app
    image: busybox
    args:
    - /bin/sh
    - -c
    - 'while true; do echo "$(date) | $(du -sh ~)" >> /var/logs/diskspace.txt; sleep 5; done;'
    volumeMounts:
    - name: log-vol
      mountPath: /var/logs
  - name: transformer
    image: busybox
    args:
    - /bin/sh
    - -c
    - 'sleep 20; while true; do while read LINE; do echo "$LINE" | cut -f2 -d"|" >> /tmp/$(date +%Y-%m-%d-%H-%M-%S)-transformed.txt; done < /var/logs/diskspace.txt; sleep 20; done;'
    volumeMounts:
    - name: log-vol
      mountPath: /var/logs
  restartPolicy: Never
```

```bash
kubectl apply -f lab/adapter.yaml
kubectl wait pod/adapter --for=condition=Ready --timeout=60s
```

### Verify

After at least 20 seconds, shell into the `transformer` container and list the transformed files:

```bash
kubectl exec adapter -c transformer -- ls /tmp
# 2024-01-01-00-00-20-transformed.txt
# ...
```

## Checklist (Score: 0/5)

- [ ] Pod `adapter` is running
- [ ] Pod has two containers: `app` and `transformer`
- [ ] Both containers share the same `emptyDir` volume mounted at `/var/logs`
- [ ] Container `app` writes to `/var/logs/diskspace.txt`
- [ ] Container `transformer` produces timestamped files in `/tmp`
