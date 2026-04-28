# Question 131

> **Solve this question on:** `ckad-lab-12`

Create a *PersistentVolume* named `project-pv` with a capacity of 2Gi, `accessMode` `ReadWriteOnce`, `storageClassName` `moon-retain`, and the `hostPath` at `/Volumes/Data`.

Create a *PersistentVolumeClaim* named `project-pvc` in *Namespace* `moon` with a storage request of 2Gi, `accessMode` `ReadWriteOnce`, and `storageClassName` `moon-retain`.

Finally, create a new *Deployment* named `project-deploy` in *Namespace* `moon` which mounts that volume at `/tmp/project-data`. The *Pods* of the *Deployment* should use image `nginx:1.14.2`.
