# Question 58

> **Solve this question on:** `ckad-lab-58`

Create a namespace called `storage-namespace`.

Create a PersistentVolume called `my-pv` with `5Gi` storage using hostPath `/mnt/my-host`.

Create a PersistentVolumeClaim called `my-pvc` with `2Gi` storage (storageClass: `manual`, accessMode: `ReadWriteOnce`).

Create a pod called `storage-pod` using the `nginx` image. Mount the PersistentVolumeClaim onto `/my-mount` inside the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
