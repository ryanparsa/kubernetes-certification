# Question 17

> **Solve this question on:** `ckad-lab-17`

For this storage-related task, you need to provision persistent storage resources.

Create a PersistentVolume named `pv-storage` with exactly `1Gi` capacity. Configure it with access mode `ReadWriteOnce` to allow read-write access by a single node.

Use `hostPath` type pointing to the directory `/mnt/data` on the node.

Set the reclaim policy to `Retain` so that the storage resource is not automatically deleted when the PV is released.

This PV will be used by applications requiring persistent storage in the cluster.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
