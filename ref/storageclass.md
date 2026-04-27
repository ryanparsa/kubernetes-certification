# StorageClass and Dynamic Provisioning

A StorageClass tells Kubernetes how to dynamically provision a PV when a PVC requests
it by `storageClassName`.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"   # make this the default
provisioner: rancher.io/local-path    # depends on the environment
reclaimPolicy: Delete                 # applied to dynamically created PVs
volumeBindingMode: WaitForFirstConsumer  # delay binding until pod is scheduled
allowVolumeExpansion: true
```

### Default StorageClass

If a PVC omits `storageClassName`, it uses the cluster's default StorageClass.
Only one StorageClass should have `is-default-class: "true"`.

```bash
# View StorageClasses
kubectl get storageclass

# Check which is default
kubectl get sc -o wide
```

### Dynamic provisioning flow

```
PVC created (with storageClassName: fast)
  → StorageClass controller calls provisioner
    → Provisioner creates the actual storage (disk, directory, etc.)
      → PV is auto-created and bound to the PVC
        → Pod can mount the PVC
```

### PVC with dynamic provisioning

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
  namespace: my-app
spec:
  storageClassName: fast      # references the StorageClass above
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

---

