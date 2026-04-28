# Question 70

> **Solve this question on:** `ckad-lab-70`

1. Create a *Pod* named `nginx-readiness` using the `nginx` image with a **readiness probe** that performs an HTTP GET on path `/` at port `80`.

2. Create a *Pod* named `nginx-liveness` using the `nginx` image with a **liveness probe** that executes the command `ls`. Set `initialDelaySeconds: 30` and `periodSeconds: 5` on the liveness probe.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
