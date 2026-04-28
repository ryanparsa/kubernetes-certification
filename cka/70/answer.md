## Answer

**Reference:** <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>

### Create the PersistentVolume

```yaml
# lab/task-pv-volume.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
spec:
  storageClassName: manual
  capacity:
    storage: 10Mi
  accessModes:
  - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

```bash
kubectl apply -f lab/task-pv-volume.yaml
kubectl get pv task-pv-volume
# NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS
# task-pv-volume   10Mi       RWO            Retain           Available           manual
```

### Create the PersistentVolumeClaim

```yaml
# lab/task-pv-claim.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: manual
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
```

```bash
kubectl apply -f lab/task-pv-claim.yaml
kubectl get pvc task-pv-claim
# NAME            STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS
# task-pv-claim   Bound    task-pv-volume   10Mi       RWO            manual
```

### Create the Pod using the PVC

```yaml
# lab/task-pv-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
  - name: task-pv-storage
    persistentVolumeClaim:
      claimName: task-pv-claim
  containers:
  - name: task-pv-pod
    image: nginx
    ports:
    - containerPort: 80
    volumeMounts:
    - mountPath: "/usr/share/nginx/html"
      name: task-pv-storage
```

```bash
kubectl apply -f lab/task-pv-pod.yaml
kubectl get pod task-pv-pod
# NAME          READY   STATUS    RESTARTS   AGE
# task-pv-pod   1/1     Running   0          10s
```

## Checklist (Score: 0/6)

- [ ] PersistentVolume `task-pv-volume` exists with capacity `10Mi` and `ReadWriteOnce`
- [ ] PersistentVolume uses `storageClassName: manual` and hostPath `/mnt/data`
- [ ] PersistentVolumeClaim `task-pv-claim` exists with `storageClassName: manual`
- [ ] PVC `task-pv-claim` is in `Bound` status bound to `task-pv-volume`
- [ ] Pod `task-pv-pod` is running using the `nginx` image
- [ ] Pod `task-pv-pod` mounts `task-pv-claim` at `/usr/share/nginx/html`
