# Question 9

> **Solve this question on:** `cks-lab-9`

Create a pod named `secure-container` in the `os-hardening` namespace using the `nginx` image with the following security settings:

1. The container should drop ALL capabilities and only add back the `NET_BIND_SERVICE` capability
2. The container should use a read-only root filesystem
3. The container should run as user ID 1000 and group ID 3000

Ensure the container can start successfully and serve traffic on port 80.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
