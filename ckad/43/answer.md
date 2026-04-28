## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/

### Create the namespace

```bash
kubectl create namespace state
```

### Create PV, PVC, and Pod

```yaml
# lab/43.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: state
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: db-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-pvc
  namespace: state
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
---
apiVersion: v1
kind: Pod
metadata:
  name: db-pod
  namespace: state
spec:
  containers:
  - name: mysql
    image: mysql:5.7
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: rootpassword
    - name: MYSQL_DATABASE
      value: mydb
    - name: MYSQL_USER
      value: myuser
    - name: MYSQL_PASSWORD
      value: mypassword
    volumeMounts:
    - name: mysql-storage
      mountPath: /var/lib/mysql
  volumes:
  - name: mysql-storage
    persistentVolumeClaim:
      claimName: db-pvc
```

```bash
kubectl apply -f lab/43.yaml
kubectl wait pod/db-pod -n state --for=condition=Ready --timeout=120s
```

### Verify

```bash
kubectl get pv db-pv
kubectl get pvc db-pvc -n state
kubectl get pod db-pod -n state
```

## Checklist (Score: 0/6)

- [ ] Namespace `state` exists
- [ ] PersistentVolume `db-pv` has capacity `1Gi`, access mode `ReadWriteOnce`, hostPath `/mnt/data`, and reclaim policy `Retain`
- [ ] PersistentVolumeClaim `db-pvc` requests `500Mi` with access mode `ReadWriteOnce`
- [ ] Pod `db-pod` uses image `mysql:5.7`
- [ ] Pod mounts the PVC at `/var/lib/mysql`
- [ ] Pod has correct environment variables (`MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`)
