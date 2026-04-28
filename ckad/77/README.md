# Question 77

> **Solve this question on:** `ckad-lab-77`

1. Create a *PersistentVolume* named `pv` with the following attributes:
   - Access mode: `ReadWriteMany`
   - Storage class name: `shared`
   - Capacity: `512Mi`
   - Host path: `/data/config`

2. Create a *PersistentVolumeClaim* named `pvc` that requests `256Mi` of storage from the *PersistentVolume* above. Ensure the claim is **Bound** after creation.

3. Create a *Pod* named `app` using the image `nginx`. Mount the *PersistentVolumeClaim* at the path `/var/app/config` inside the container.

4. Describe the *Pod* and confirm in the events that the *PersistentVolume* was mounted successfully.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
