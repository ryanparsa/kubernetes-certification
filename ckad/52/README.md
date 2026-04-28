# Question 52

> **Solve this question on:** `ckad-lab-52`

Create a Pod named `health-check-pod` in the `health-checks` namespace with the following specifications:

1. Use image `nginx`
2. Configure startup probe: HTTP GET on port `80`, `initialDelaySeconds=10`, `periodSeconds=3`, `failureThreshold=3`
3. Configure liveness probe: HTTP GET on port `80`, `initialDelaySeconds=15`, `periodSeconds=5`, `failureThreshold=3`
4. Configure readiness probe: HTTP GET on port `80`, `initialDelaySeconds=5`, `periodSeconds=3`, `failureThreshold=3`

Ensure the namespace exists before creating the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
