# Question 40

> **Solve this question on:** `cka-lab-40`

Create a *StorageClass* named `fast-storage` with the provisioner `kubernetes.io/no-provisioner`.

Create a *PersistentVolumeClaim* named `data-pvc` in the `storage` namespace that uses this StorageClass.

Set the access mode to `ReadWriteOnce` and request `1Gi` of storage.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
