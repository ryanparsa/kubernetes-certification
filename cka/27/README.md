# Question 10

> **Solve this question on:** the "cka-lab" kind cluster

There is a backup *Job* which needs to be adjusted to use a *PVC* to store backups.

Create a *StorageClass* named `local-backup` which uses `provisioner: rancher.io/local-path` and `volumeBindingMode: WaitForFirstConsumer`. To prevent possible data loss the *StorageClass* should keep a *PV* retained even if a bound *PVC* is deleted.

Adjust the *Job* at `cka/27/lab/backup.yaml` to use a *PVC* which request `50Mi` storage and uses the new *StorageClass*.

Deploy your changes, verify the *Job* completed once and the *PVC* was bound to a newly created *PV*.

> [!NOTE]
> To re-run a *Job*, delete it and create it again.

> [!NOTE]
> The abbreviation *PV* stands for *PersistentVolume* and *PVC* for *PersistentVolumeClaim*.

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`
