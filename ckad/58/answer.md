## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

### Create the namespace

```bash
kubectl create namespace storage-namespace
```

### Create the PersistentVolume

```yaml
# lab/58-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  storageClassName: manual
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/my-host"
```

```bash
kubectl apply -f lab/58-pv.yaml
```

### Create the PersistentVolumeClaim

```yaml
# lab/58-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
  namespace: storage-namespace
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```

```bash
kubectl apply -f lab/58-pvc.yaml
```

### Create the Pod

```yaml
# lab/58-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: storage-pod
  namespace: storage-namespace
spec:
  volumes:
    - name: my-volume
      persistentVolumeClaim:
        claimName: my-pvc
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - mountPath: "/my-mount"
          name: my-volume
```

```bash
kubectl apply -f lab/58-pod.yaml
kubectl wait pod/storage-pod -n storage-namespace --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pv my-pv
kubectl get pvc my-pvc -n storage-namespace
kubectl describe pod storage-pod -n storage-namespace | grep -i mounts -A 2
```

## Checklist (Score: 0/4)

- [ ] PersistentVolume `my-pv` exists with `5Gi` capacity and hostPath `/mnt/my-host`
- [ ] PersistentVolumeClaim `my-pvc` exists in `storage-namespace` and is `Bound`
- [ ] Pod `storage-pod` exists in `storage-namespace` and is `Running`
- [ ] Volume is mounted at `/my-mount` inside `storage-pod`
