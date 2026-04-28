# Question 105

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Create a new *PersistentVolume* named `safari-pv`. It should have a capacity of `2Gi`, accessMode `ReadWriteOnce`, hostPath `/Volumes/Data` and no `storageClassName` defined.

Next create a new *PersistentVolumeClaim* in *Namespace* `project-tiger` named `safari-pvc`. It should request `2Gi` storage, accessMode `ReadWriteOnce` and should not define a `storageClassName`. The PVC should bound to the PV correctly.

Finally create a new *Deployment* named `safari` in *Namespace* `project-tiger` which mounts that volume at `/tmp/safari-data`. The *Pod* of that *Deployment* should be of image `httpd:2.4.41-alpine`.
