# Question 43

> **Solve this question on:** `cka-lab-43`

Create a *NetworkPolicy* named `db-policy` in the `networking` namespace that:

1. Allows pods with label `role=frontend` to connect to pods with label `role=db` on port `3306`
2. Denies all other ingress traffic to pods with label `role=db`

Ensure the policy is correctly applied to pods with the matching labels.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
