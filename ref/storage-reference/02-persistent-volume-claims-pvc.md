# Kubernetes Storage Reference — 2. Persistent Volume Claims (PVC)

> Part of [Kubernetes Storage Reference](../Storage Reference.md)


A PVC is a request for storage by a user. Kubernetes binds the PVC to a matching PV.

### Binding rules

A PVC binds to a PV when **all** of the following match:
1. `accessModes` — PV must support all access modes requested by PVC
2. `storage` — PV capacity ≥ PVC request
3. `storageClassName` — must match exactly (both empty, or same class name)
4. `selector` — optional label selector on PV metadata

### PVC YAML

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: safari-pvc
  namespace: project-t230
spec:
  storageClassName: ""        # empty: only binds to PVs with no storageClassName
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```

### Check binding status

```bash
kubectl -n project-t230 get pv,pvc
# NAME                        CAPACITY   STATUS   CLAIM
# persistentvolume/safari-pv  2Gi        Bound    project-t230/safari-pvc
#
# NAME                              STATUS   VOLUME      CAPACITY
# persistentvolumeclaim/safari-pvc  Bound    safari-pv   2Gi
```

### Mount a PVC into a Pod / Deployment

```yaml
spec:
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: safari-pvc
  containers:
  - name: app
    image: httpd:2-alpine
    volumeMounts:
    - name: data
      mountPath: /tmp/safari-data
```

---

