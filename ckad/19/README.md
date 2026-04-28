# Question 19

> **Solve this question on:** `ckad-lab-19`

An application team needs storage for their database.

Create a PersistentVolumeClaim named `pvc-app` in the `storage-test` namespace that will request storage from the previously created StorageClass.

The PVC should request exactly `500Mi` of storage capacity and use the `ReadWriteOnce` access mode to ensure data consistency.

Make sure to specify the `fast-storage` StorageClass as the storage class for this claim.

This PVC will be used by a database application that requires persistent storage.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
