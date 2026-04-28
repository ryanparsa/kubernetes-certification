# Question 43

> **Solve this question on:** `ckad-lab-43`

Set up persistent storage for a database application in the `state` namespace:

1. Create a PersistentVolume named `db-pv` with storage capacity of `1Gi`, access mode `ReadWriteOnce`, hostPath type pointing to `/mnt/data`, and reclaim policy `Retain`
2. Create a PersistentVolumeClaim named `db-pvc` that requests `500Mi` storage with access mode `ReadWriteOnce`
3. Create a Pod named `db-pod` using the `mysql:5.7` image that mounts the PVC at `/var/lib/mysql`
4. Set the following environment variables for the pod:
   - `MYSQL_ROOT_PASSWORD=rootpassword`
   - `MYSQL_DATABASE=mydb`
   - `MYSQL_USER=myuser`
   - `MYSQL_PASSWORD=mypassword`

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
