## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/

### Create the namespace

```bash
kubectl create namespace storage-task
```

### Create the PVC

```yaml
# lab/48-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: storage-task
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```

```bash
kubectl apply -f lab/48-pvc.yaml
```

### Create the Pod

```yaml
# lab/48-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-pod
  namespace: storage-task
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: data
      mountPath: /usr/share/nginx/html
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-pvc
```

```bash
kubectl apply -f lab/48-pod.yaml
kubectl wait pod data-pod -n storage-task --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pvc data-pvc -n storage-task
kubectl get pod data-pod -n storage-task
```

## Checklist (Score: 0/5)

- [ ] PVC `data-pvc` exists in `storage-task` namespace
- [ ] PVC uses StorageClass `standard` with `ReadWriteOnce` and `2Gi`
- [ ] Pod `data-pod` exists in `storage-task` namespace
- [ ] Pod uses the `nginx` image
- [ ] Pod mounts the PVC as volume `data` at `/usr/share/nginx/html`
