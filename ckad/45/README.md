# Question 45

> **Solve this question on:** `ckad-lab-45`

There is a deployment named `broken-deployment` in the `troubleshooting` namespace that is not functioning correctly. The deployment should have `3` replicas of `nginx:1.19` pods, but it's failing.

Find and fix the issue(s) with the deployment. Possible issues might include:

- Incorrect image name or tag
- Resource constraints that can't be satisfied
- Configuration problems with the pod template
- Network policy restrictions

Ensure the deployment functions correctly with 3 replicas running.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
