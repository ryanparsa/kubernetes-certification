## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims

### Create the namespace (if not present)

```bash
kubectl create namespace storage-test --dry-run=client -o yaml | kubectl apply -f -
```

### Create the PersistentVolumeClaim

```yaml
# lab/pvc-app.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-app
  namespace: storage-test
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
  storageClassName: fast-storage
```

```bash
kubectl apply -f lab/pvc-app.yaml
```

### Verify

```bash
kubectl get pvc pvc-app -n storage-test
kubectl describe pvc pvc-app -n storage-test
```

## Checklist (Score: 0/4)

- [ ] PersistentVolumeClaim `pvc-app` exists in namespace `storage-test`
- [ ] PVC requests `500Mi` of storage
- [ ] PVC has access mode `ReadWriteOnce`
- [ ] PVC uses StorageClass `fast-storage`
