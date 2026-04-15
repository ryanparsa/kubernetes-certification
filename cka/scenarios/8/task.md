# Task 8 — Storage

**Context:** Cluster `cka-task-8` (`export KUBECONFIG=$PWD/kubeconfig`)

Namespace `storage` already exists. The cluster's default `StorageClass` has been
unmarked as default — you must create your own.

## Objective

In namespace `storage`, create:

1. A `StorageClass` named **`fast`** that uses provisioner **`rancher.io/local-path`**
   (the same provisioner kind ships) with `volumeBindingMode: WaitForFirstConsumer`.
2. A `PersistentVolumeClaim` named **`data-pvc`** in namespace `storage`:
   - Access mode: `ReadWriteOnce`
   - Size: `500Mi`
   - StorageClass: `fast`
3. A `Pod` named **`data-pod`** in namespace `storage`:
   - Image: `nginx:1.27-alpine`
   - Mount `data-pvc` at **`/data`** in the container.

The PVC must reach `Bound` and the Pod must reach `Running`.

## Verify

```
./test.sh
```
