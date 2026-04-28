# Question 85

> **Solve this question on:** the `cka-lab` kind cluster

Create a new *PersistentVolume* named `safari-pv` with:
- Capacity: `2Gi`
- Access mode: `ReadWriteOnce`
- Host path: `/Volumes/Data`
- No `storageClassName`

Then create a *PersistentVolumeClaim* named `safari-pvc` in *Namespace* `project-tiger` that binds to it, and a *Pod* named `safari` that mounts the PVC.
