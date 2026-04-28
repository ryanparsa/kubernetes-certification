# Question 27

> **Solve this question on:** `ckad-lab-27`

To ensure application reliability, the team needs to implement health checking for a critical service.

Create a Pod named `health-pod` in namespace `workloads` using the `emilevauge/whoami` image with the following health monitoring configuration:

1. A liveness probe that performs an HTTP GET request to the path `/healthz` on port `80` every `15` seconds to determine if the container is alive. If this check fails, Kubernetes will restart the container.

2. A readiness probe that checks if the container is ready to serve traffic by testing if port `80` is open and accepting connections every `10` seconds.

Configure appropriate initial delay, timeout, and failure threshold values based on best practices.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
