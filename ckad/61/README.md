# Question 61

> **Solve this question on:** `ckad-lab-61`

Create a namespace called `service-namespace`.

Create a pod called `service-pod` using the `nginx` image, exposing port `80`, with label `tier=web`.

Create a ClusterIP service called `my-service` that routes traffic to `service-pod` and exposes port `8080` (target port `80`).

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
