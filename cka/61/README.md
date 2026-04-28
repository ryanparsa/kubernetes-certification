# Question 61

> **Solve this question on:** `cka-lab-61`

Configure resource management in the `limits` namespace:

1. Create a LimitRange with:
   - Default request: CPU `100m`, Memory `128Mi`
   - Default limit: CPU `200m`, Memory `256Mi`
   - Max limit: CPU `500m`, Memory `512Mi`

2. Create a ResourceQuota for the namespace:
   - Max total CPU: `2`
   - Max total memory: `2Gi`
   - Max number of pods: `5`

3. Create a deployment named `test-limits` with `2` replicas using the `nginx` image to verify the limits are applied

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
