# Kubernetes Storage Reference

Reference for Persistent Volumes, Persistent Volume Claims, StorageClasses, volume
types, and CSI — everything that keeps data alive beyond a pod's lifetime.

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

## 2. Persistent Volume Claims (PVC)

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

## 3. StorageClass and Dynamic Provisioning

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

## 4. Volume Types

### emptyDir

Temporary scratch space shared between containers in the same Pod. Deleted when the pod
is removed. Survives container restarts.

```yaml
volumes:
- name: shared-data
  emptyDir: {}
  # emptyDir:
  #   medium: Memory   # RAM-backed tmpfs
  #   sizeLimit: 128Mi
```

### hostPath

Mounts a directory from the **node's** filesystem. Data persists as long as the node
exists but is NOT portable across nodes.

```yaml
volumes:
- name: host-log
  hostPath:
    path: /var/log/myapp
    type: DirectoryOrCreate   # Directory | File | Socket | CharDevice | BlockDevice
```

> ⚠️ Security risk: gives pod access to node filesystem. Avoid in production.

### configMap

Mount a ConfigMap as files.

```yaml
volumes:
- name: config
  configMap:
    name: my-config
    items:
    - key: app.properties
      path: application.properties   # filename inside the mount
```

### secret

Mount a Secret as files. Files are base64-decoded automatically.

```yaml
volumes:
- name: tls-certs
  secret:
    secretName: my-tls
    defaultMode: 0400    # restrict permissions
```

### projected

Combines multiple sources (serviceAccountToken, configMap, secret, downwardAPI) into
a single mount point.

```yaml
volumes:
- name: token-and-ca
  projected:
    sources:
    - serviceAccountToken:
        path: token
        expirationSeconds: 3600
        audience: api
    - configMap:
        name: kube-root-ca.crt
        items:
        - key: ca.crt
          path: ca.crt
    - downwardAPI:
        items:
        - path: namespace
          fieldRef:
            fieldPath: metadata.namespace
```

> This is the default volume injected into every pod at
> `/var/run/secrets/kubernetes.io/serviceaccount/`.

### nfs

```yaml
volumes:
- name: nfs-vol
  nfs:
    server: nfs-server.example.com
    path: /exports/mydata
    readOnly: false
```

---

## 5. CSI (Container Storage Interface)

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

## 6. Volume Expansion

```bash
# Edit PVC to request more storage (StorageClass must have allowVolumeExpansion: true)
kubectl edit pvc my-pvc
# Change: resources.requests.storage: 20Gi

# Check expansion status
kubectl describe pvc my-pvc
# Conditions: FileSystemResizePending → resize happens on next pod mount
```

---

## 7. Imperative Commands

```bash
# Create a PVC
kubectl -n my-app create -f pvc.yaml

# List PVs and PVCs
kubectl get pv
kubectl get pvc -A

# Describe a PV (see events)
kubectl describe pv safari-pv

# Delete a PVC (PV behaviour depends on reclaimPolicy)
kubectl delete pvc safari-pvc -n project-t230

# Manually reclaim a Released PV (Retain policy)
# 1. Delete the PV
kubectl delete pv safari-pv
# 2. Clean up the storage manually
# 3. Re-create the PV
```

---

## 8. Quick Reference

| PVC not binding? | Check |
|---|---|
| Wrong storageClassName | Both PV and PVC must have identical `storageClassName` |
| Insufficient capacity | PV size must be ≥ PVC request |
| Access mode mismatch | PV must include all access modes in PVC |
| PV already bound | Each PV can only bind to one PVC |
| Selector mismatch | Check `spec.selector` on PVC and labels on PV |

```bash
# Debug binding
kubectl describe pvc my-pvc   # look at Events section
kubectl get pv                # check STATUS column
```
