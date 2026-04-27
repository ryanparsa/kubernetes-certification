# Kubernetes Storage Reference

[← Back to index](../README.md)

---

## 1. Persistent Volumes (PV)

A PersistentVolume is a cluster-level storage resource provisioned by an administrator
(static) or by a StorageClass (dynamic). It has its own lifecycle independent of any pod.

### PV Access Modes

| Mode | Abbreviation | Meaning |
|---|---|---|
| `ReadWriteOnce` | RWO | Mounted read-write by **one node** at a time |
| `ReadOnlyMany` | ROX | Mounted read-only by **many nodes** simultaneously |
| `ReadWriteMany` | RWX | Mounted read-write by **many nodes** simultaneously |
| `ReadWriteOncePod` | RWOP | Mounted read-write by **one pod** at a time (Kubernetes 1.22+) |

> Not all storage backends support all access modes. `hostPath` only supports RWO.
> NFS supports RWX; most block storage (EBS, GCE PD) supports only RWO.

### PV Reclaim Policies

| Policy | Effect after PVC is deleted |
|---|---|
| `Retain` | PV stays, status → `Released`; admin must manually reclaim or delete |
| `Delete` | PV and the underlying storage asset are automatically deleted |
| `Recycle` (deprecated) | Basic scrub (`rm -rf /data/*`) then makes PV available again |

### PV Phases

| Phase | Meaning |
|---|---|
| `Available` | Free, not yet bound to a PVC |
| `Bound` | Bound to a specific PVC |
| `Released` | PVC deleted but PV not yet reclaimed |
| `Failed` | Auto-reclamation failed |

### PV YAML (static provisioning)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: safari-pv
spec:
  storageClassName: ""        # empty = not managed by any StorageClass
  capacity:
    storage: 2Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /Volumes/Data
```

---
