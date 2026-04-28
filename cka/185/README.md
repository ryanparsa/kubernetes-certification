# Question 185

> **Solve this question on:** `ssh cka7868`

Create a new *PersistentVolume* named `safari-pv`. It should have a capacity of `2Gi`, accessMode `ReadWriteOnce`, hostPath `/Volumes/Data` and no `storageClassName` defined.

Next create a new *PersistentVolumeClaim* in *Namespace* `project-tiger` named `safari-pvc`. It should request `2Gi` storage, accessMode `ReadWriteOnce` and should not define a `storageClassName`. The PVC should bind to the PV correctly.

Finally create a new *Deployment* named `safari` in *Namespace* `project-tiger` which mounts that volume at `/tmp/safari-data`. The *Pods* of that *Deployment* should be of image `httpd:2.4-alpine`.
