# Question 1

> **Solve this question on:** `cks-lab-1`

Create a NetworkPolicy named `secure-backend` in the `network-security` namespace that restricts access to pods with label `app=backend` to only allow ingress traffic from pods with label `app=frontend` on port 8080.

Additionally, ensure that these backend pods can only make egress connections to pods with label `app=database` on port 5432.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
