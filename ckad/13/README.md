# Question 13

> **Solve this question on:** `ckad-lab-13`

Perform the following storage tasks:

1. Create a PersistentVolume named `task-pv` with:
   - `storageClassName: manual`
   - `capacity: storage: 1Gi`
   - `accessModes: ReadWriteOnce`
   - `hostPath: path: /mnt/data`

2. Create a PersistentVolumeClaim named `task-pvc` that requests `500Mi` of storage with `storageClassName: manual` and `accessModes: ReadWriteOnce`.

3. Create a pod named `pv-pod` with image `nginx` that mounts the `task-pvc` volume at `/usr/share/nginx/html`. Verify the PVC is bound and the pod is running.
