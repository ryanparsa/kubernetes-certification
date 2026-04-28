## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/

### Create the namespace

```bash
kubectl create namespace storage
```

### Create the StorageClass

```yaml
# lab/fast-storage.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/no-provisioner
```

```bash
kubectl apply -f lab/fast-storage.yaml
```

### Create the PersistentVolumeClaim

```yaml
# lab/data-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: storage
spec:
  storageClassName: fast-storage
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```bash
kubectl apply -f lab/data-pvc.yaml
```

### Verify

```bash
kubectl get sc fast-storage
kubectl get pvc data-pvc -n storage
```

## Checklist (Score: 0/4)

- [ ] StorageClass `fast-storage` exists with provisioner `kubernetes.io/no-provisioner`
- [ ] PVC `data-pvc` exists in namespace `storage`
- [ ] PVC uses StorageClass `fast-storage`
- [ ] PVC requests `1Gi` with access mode `ReadWriteOnce`
