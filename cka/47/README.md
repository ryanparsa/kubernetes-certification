# Question 47

> **Solve this question on:** `cka-lab-47`

Create a pod named `health-check` in the `default` namespace using the `nginx` image with the following health check configuration:

- Liveness probe: HTTP GET on path `/` port `80` with initial delay of `5` seconds
- Readiness probe: HTTP GET on path `/` port `80` with initial delay of `5` seconds

Ensure the pod is running with both probes functioning correctly.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
