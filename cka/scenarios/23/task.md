# Task 23 — Storage: Manual PV & PVC

**Context:** Cluster `cka-task-23` (`export KUBECONFIG=$PWD/kubeconfig`)

You need to mount a specific directory `/mnt/data` from the control-plane node into
a Pod for persistent storage.

## Objective

1. Create a `PersistentVolume` named **`manual-pv`**:
   - Capacity: **1Gi**
   - Access Mode: **ReadWriteOnce**
   - StorageClass: **`local-storage`**
   - Reclaim Policy: **Retain**
   - Type: **`hostPath`** with path **`/mnt/data`**
2. Create a `PersistentVolumeClaim` named **`manual-pvc`** in the `default` namespace:
   - Request: **1Gi**
   - Access Mode: **ReadWriteOnce**
   - StorageClass: **`local-storage`** (must match PV)
3. Create a `Pod` named **`storage-pod`** in the `default` namespace:
   - Image: **`nginx:1.27-alpine`**
   - Mount the PVC at **`/usr/share/nginx/html`**.

The PVC must reach `Bound` and the Pod must reach `Running`.

## Verify

```
./test.sh
```
