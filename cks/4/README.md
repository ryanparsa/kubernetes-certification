# Question 4

> **Solve this question on:** `cks-lab-4`

Protect the Kubernetes node metadata from being accessed by pods. Create a NetworkPolicy named `block-metadata` in the `metadata-protect` namespace that blocks outbound access from all pods to the Kubernetes metadata endpoint (usually at 169.254.169.254).

Verify your implementation by creating a pod named `test-pod` in the same namespace using the `busybox` image with a command that sleeps for 3600 seconds.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
