# Volume Expansion

```bash
# Edit PVC to request more storage (StorageClass must have allowVolumeExpansion: true)
kubectl edit pvc my-pvc
# Change: resources.requests.storage: 20Gi

# Check expansion status
kubectl describe pvc my-pvc
# Conditions: FileSystemResizePending → resize happens on next pod mount
```

---

