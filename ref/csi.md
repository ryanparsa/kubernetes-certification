# CSI (Container Storage Interface)

CSI decouples storage drivers from the Kubernetes core. A CSI driver runs as a pod
(usually a DaemonSet + StatefulSet/Deployment) and exposes a Unix socket.

### Key components

| Component | Purpose |
|---|---|
| CSI Driver (node plugin) | DaemonSet on every node; handles `NodeStageVolume`, `NodePublishVolume` |
| CSI Controller | Deployment; handles provisioning, attach/detach |
| External provisioner | Sidecar that watches PVCs and calls `CreateVolume` |
| External attacher | Sidecar that calls `ControllerPublishVolume` (attach to node) |

### CSI PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-csi-pvc
spec:
  storageClassName: csi-driver-storageclass
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### Check CSI drivers installed

```bash
kubectl get csidrivers
kubectl get csinode
```

---

