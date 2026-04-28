# Question 64

> **Solve this question on:** `cka-lab-64`

Configure network policies in the `network` namespace:

1. Create a deployment named `web` using the `nginx` image with label `app=web`
2. Create a deployment named `api` using the `nginx` image with label `app=api`
3. Create a deployment named `db` using the `postgres` image with label `app=db` and environment variable `POSTGRES_HOST_AUTH_METHOD=trust`
4. Create NetworkPolicies to enforce the following traffic rules:
   - `web` can communicate only with `api`
   - `api` can communicate only with `db`
   - All other traffic between pods is denied

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
