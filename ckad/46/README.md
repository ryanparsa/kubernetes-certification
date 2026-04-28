# Question 46

> **Solve this question on:** the "ckad-lab-46" kind cluster

Create a *NetworkPolicy* in the `networking` *Namespace* that restricts access to the `secure-db` *Pod* with label `app=db` as follows:

1. Allow ingress traffic only from *Pods* with the label `role=frontend` on port `5432`
2. Allow egress traffic only to *Pods* with the label `role=monitoring` on port `8080`
3. Deny all other traffic

Then create three *Pods* for testing:

- A *Pod* named `secure-db` with label `app=db` using image `postgres:12`
- A *Pod* named `frontend` with label `role=frontend` using image `nginx`
- A *Pod* named `monitoring` with label `role=monitoring` using image `nginx`

Ensure the *Namespace* exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
