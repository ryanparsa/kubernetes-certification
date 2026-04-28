# Question 67

> **Solve this question on:** `cka-lab-67`

A deployment named `failing-app` has been created in the `troubleshoot` namespace but pods are not running. The deployment uses image `nginx:1.25` and should have `3` replicas.

Fix the following issues:

1. The deployment is using an incorrect container port (`8080` instead of `80`)
2. The pods are failing due to insufficient memory (current limit is `64Mi`, should be `256Mi`)
3. There is a misconfigured liveness probe checking port `8080` instead of `80`

Ensure all pods are running successfully after applying the fixes.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
