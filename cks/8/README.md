# Question 8

> **Solve this question on:** `cks-lab-8`

Restrict access to the Kubernetes API server by creating a NetworkPolicy named `api-server-policy` in the `api-restrict` namespace that denies all egress traffic to the Kubernetes API server except from pods with the label `role=admin`.

Create a pod named `admin-pod` with label `role=admin` and a pod named `restricted-pod` with label `role=restricted` in the same namespace. Both pods should use the `busybox` image and sleep for 3600 seconds.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
