# Question 50

> **Solve this question on:** `cka-lab-50`

Create a PersistentVolume named `manual-pv` with the following specifications:

- Storage: `1Gi`
- Access Mode: `ReadWriteOnce`
- Host Path: `/mnt/data`
- Node Affinity: Must run on node `k3d-cluster-agent-0`

Then create a PersistentVolumeClaim named `manual-pvc` that binds to this PV.

Finally, create a Pod named `manual-pod` using the `busybox` image that mounts this PVC at `/data` and runs the command `sleep 3600`.

All resources should be in the `manual-storage` namespace (except the PersistentVolume which is cluster-scoped).

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
