# Question 45

> **Solve this question on:** `ckad-lab-45`

There is a *Deployment* named `broken-deployment` in the `troubleshooting` *Namespace* that is not functioning correctly. The *Deployment* should have `3` replicas of `nginx:1.19` *Pods*, but it's failing.

Find and fix the issue(s) with the *Deployment*. Possible issues might include:

- Incorrect image name or tag
- Resource constraints that can't be satisfied
- Configuration problems with the *Pod* template
- *NetworkPolicy* restrictions

Ensure the *Deployment* functions correctly with 3 replicas running.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
