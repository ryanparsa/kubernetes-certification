## Answer

**Reference:** <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>

### Create the PersistentVolume

```yaml
# lab/pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv
spec:
  capacity:
    storage: 512Mi
  accessModes:
  - ReadWriteMany
  storageClassName: shared
  hostPath:
    path: /data/config
```

```bash
kubectl apply -f lab/pv.yaml
kubectl get pv pv
# NAME   CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   AGE
# pv     512Mi      RWX            Retain           Available           shared         4s
```

### Create the PersistentVolumeClaim

```yaml
# lab/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 256Mi
  storageClassName: shared
```

```bash
kubectl apply -f lab/pvc.yaml
kubectl get pvc pvc
# NAME   STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
# pvc    Bound    pv       512Mi      RWX            shared         2s
```

### Create the Pod

```yaml
# lab/app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - image: nginx
    name: app
    volumeMounts:
    - mountPath: /var/app/config
      name: configpvc
    resources: {}
  volumes:
  - name: configpvc
    persistentVolumeClaim:
      claimName: pvc
  dnsPolicy: ClusterFirst
  restartPolicy: Never
```

```bash
kubectl apply -f lab/app.yaml
kubectl wait pod/app --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl describe pod app | grep -A5 Events
# Normal  SuccessfulAttachVolume  ...  MountVolume.SetUp succeeded for volume "pv"
```

## Checklist (Score: 0/6)

- [ ] *PersistentVolume* `pv` exists with capacity `512Mi` and access mode `ReadWriteMany`
- [ ] *PersistentVolume* uses storage class `shared` and host path `/data/config`
- [ ] *PersistentVolumeClaim* `pvc` exists and is **Bound** to `pv`
- [ ] *PersistentVolumeClaim* requests `256Mi` with storage class `shared`
- [ ] Pod `app` is running
- [ ] Pod `app` mounts the PVC at `/var/app/config`
