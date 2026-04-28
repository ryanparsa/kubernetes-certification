# Question 48

> **Solve this question on:** `cka-lab-48`

Create a Dynamic PVC named `data-pvc` with the following specifications:

- Storage Class: `standard`
- Access Mode: `ReadWriteOnce`
- Storage Request: `2Gi`

Then create a Pod named `data-pod` using the `nginx` image that mounts this PVC as volume with name `data` at `/usr/share/nginx/html`.

Ensure both the PVC and Pod are in the `storage-task` namespace.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
