# Question 70

> **Solve this question on:** `cka-lab-70`

Perform the following steps:

1. Create a *PersistentVolume* named `task-pv-volume` with:
   - Storage: `10Mi`
   - Access mode: `ReadWriteOnce`
   - Storage class: `manual`
   - Host path: `/mnt/data`

2. Create a *PersistentVolumeClaim* named `task-pv-claim` that requests `10Mi` with access mode `ReadWriteOnce` and storage class `manual`. Verify it binds to `task-pv-volume`.

3. Create a *Pod* named `task-pv-pod` with the `nginx` image that uses `task-pv-claim` as a volume mounted at `/usr/share/nginx/html`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
