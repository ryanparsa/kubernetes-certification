# Kubernetes Storage Reference — 6. Volume Expansion

> Part of [Kubernetes Storage Reference](../Storage Reference.md)


```bash
# Edit PVC to request more storage (StorageClass must have allowVolumeExpansion: true)
kubectl edit pvc my-pvc
# Change: resources.requests.storage: 20Gi

# Check expansion status
kubectl describe pvc my-pvc
# Conditions: FileSystemResizePending → resize happens on next pod mount
```

---

