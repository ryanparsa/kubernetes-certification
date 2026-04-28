## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/

### Create the PersistentVolume

```yaml
# lab/pv-storage.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data
```

```bash
kubectl apply -f lab/pv-storage.yaml
```

### Verify

```bash
kubectl get pv pv-storage
kubectl describe pv pv-storage
```

## Checklist (Score: 0/4)

- [ ] PersistentVolume `pv-storage` exists
- [ ] PersistentVolume has capacity `1Gi`
- [ ] PersistentVolume has access mode `ReadWriteOnce`
- [ ] PersistentVolume has reclaim policy `Retain`
