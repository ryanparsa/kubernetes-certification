# Question 79

> **Solve this question on:** `ckad-lab-79`

Create a namespace `workloads`.

In that namespace create a Pod named `web` using image `nginx:1.25`.

Add labels `app=web` and `tier=frontend` to the Pod.

Set the following resource constraints on the container:
- CPU request: `100m`, CPU limit: `250m`
- Memory request: `128Mi`, memory limit: `256Mi`

Verify the Pod is `Running` and the labels are present.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
