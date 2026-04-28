# Question 45

> **Solve this question on:** `cka-lab-45`

Create a pod named `resource-pod` in the `monitoring` namespace using the `nginx` image with the following resource requirements:

- CPU request: `100m`
- CPU limit: `200m`
- Memory request: `128Mi`
- Memory limit: `256Mi`

Ensure the pod is in the Running state with all resource constraints applied correctly.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
