# Question 18

> **Solve this question on:** `ckad-lab-18`

As part of optimizing storage resources in the cluster, create a StorageClass named `fast-storage` that will dynamically provision storage resources.

Use the provisioner `kubernetes.io/no-provisioner` for this local storage class.

Set the `volumeBindingMode` to `WaitForFirstConsumer` to delay volume binding until a pod using the PVC is created.

This storage class will be used for applications that require optimized local storage performance.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
