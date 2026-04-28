# Question 46

> **Solve this question on:** `ckad-lab-46`

Create a NetworkPolicy in the `networking` namespace that restricts access to the `secure-db` pod with label `app=db` as follows:

1. Allow ingress traffic only from pods with the label `role=frontend` on port `5432`
2. Allow egress traffic only to pods with the label `role=monitoring` on port `8080`
3. Deny all other traffic

Then create three pods for testing:

- A pod named `secure-db` with label `app=db` using image `postgres:12`
- A pod named `frontend` with label `role=frontend` using image `nginx`
- A pod named `monitoring` with label `role=monitoring` using image `nginx`

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
