# Question 59

> **Solve this question on:** `ckad-lab-59`

Create a namespace called `quota-namespace`.

Create a ResourceQuota for this namespace called `my-quota` with:
- Hard memory limit: `2Gi`
- Hard CPU limit: `500m`

Create a LimitRange for this namespace called `my-limit` that restricts Pods to a maximum of `1Gi` memory and `250m` CPU.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
