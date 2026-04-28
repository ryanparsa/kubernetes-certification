## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

### Create the PersistentVolume

```yaml
# lab/task-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  hostPath:
    path: /mnt/data
```

```bash
kubectl apply -f lab/task-pv.yaml
kubectl get pv task-pv
```

### Create the PersistentVolumeClaim

```yaml
# lab/task-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pvc
spec:
  storageClassName: manual
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

```bash
kubectl apply -f lab/task-pvc.yaml
kubectl get pvc task-pvc
```

The PVC should show status `Bound` and be bound to `task-pv`.

### Create the pod using the PVC

```yaml
# lab/pv-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pv-pod
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
      claimName: task-pvc
```

```bash
kubectl apply -f lab/pv-pod.yaml
kubectl get pod pv-pod
kubectl get pvc task-pvc
```

### Verify

```bash
# PVC should be Bound
kubectl get pvc task-pvc -o jsonpath='{.status.phase}'

# PV should show Bound to task-pvc
kubectl get pv task-pv -o jsonpath='{.status.phase}'

# Pod uses the PVC
kubectl get pod pv-pod -o jsonpath='{.spec.volumes[0].persistentVolumeClaim.claimName}'
```

## Checklist (Score: 0/3)

- [ ] PersistentVolume `task-pv` created with `storageClassName: manual`, `1Gi`, `ReadWriteOnce`, `hostPath: /mnt/data`
- [ ] PersistentVolumeClaim `task-pvc` created and status is `Bound` to `task-pv`
- [ ] Pod `pv-pod` is running with `task-pvc` mounted at `/usr/share/nginx/html`
