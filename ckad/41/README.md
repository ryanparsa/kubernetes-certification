# Question 41

> **Solve this question on:** the "ckad-lab-41" *Kind* cluster

Create a *Pod* named `probes-pod` in the `observability` *Namespace* using the image `nginx`. Configure the following probes:

1. Liveness probe: HTTP GET request to path `/healthz` on port `80`, with `initialDelaySeconds=10` and `periodSeconds=5`
2. Readiness probe: HTTP GET request to path `/` on port `80`, with `initialDelaySeconds=5` and `periodSeconds=3`

Also, configure the *Pod* with resource requests of CPU=`100m` and memory=`128Mi`, and resource limits of CPU=`200m` and memory=`256Mi`.

Ensure the *Namespace* exists before creating the *Pod*.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
