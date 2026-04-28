## Answer

**Reference:** <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>

### Create the PersistentVolume

```yaml
# lab/project-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: project-pv
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: moon-retain
  hostPath:
    path: /Volumes/Data
```

### Create the PersistentVolumeClaim

```yaml
# lab/project-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: project-pvc
  namespace: moon
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: moon-retain
  resources:
    requests:
      storage: 2Gi
```

### Create the Deployment

```yaml
# lab/project-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: project-deploy
  namespace: moon
spec:
  replicas: 1
  selector:
    matchLabels:
      app: project-deploy
  template:
    metadata:
      labels:
        app: project-deploy
    spec:
      containers:
      - name: project-deploy
        image: nginx:1.14.2
        volumeMounts:
        - name: project-data
          mountPath: /tmp/project-data
      volumes:
      - name: project-data
        persistentVolumeClaim:
          claimName: project-pvc
```

```bash
kubectl apply -f lab/project-pv.yaml
kubectl apply -f lab/project-pvc.yaml
kubectl apply -f lab/project-deploy.yaml
kubectl get pv project-pv
kubectl get pvc project-pvc -n moon
kubectl get deployment project-deploy -n moon
```

## Checklist (Score: 0/5)

- [ ] PersistentVolume `project-pv` with 2Gi capacity and `hostPath: /Volumes/Data`
- [ ] PV has `storageClassName: moon-retain` and `accessMode: ReadWriteOnce`
- [ ] PVC `project-pvc` in Namespace `moon` bound to PV
- [ ] Deployment `project-deploy` in Namespace `moon` with image `nginx:1.14.2`
- [ ] Deployment mounts PVC at `/tmp/project-data`
