# Hints — Task 8

## Hint 1
With `WaitForFirstConsumer`, the PVC stays `Pending` until a Pod that mounts it is scheduled.
That's expected — apply all three resources, then watch the PVC become `Bound` once the Pod is created.

## Solution

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: storage
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: fast
  resources:
    requests:
      storage: 500Mi
---
apiVersion: v1
kind: Pod
metadata:
  name: data-pod
  namespace: storage
spec:
  containers:
  - name: app
    image: nginx:1.27-alpine
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-pvc
```
