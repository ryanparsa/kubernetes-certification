# Question 83

> **Solve this question on:** `ckad-lab-83`

Create a namespace `network-test`.

Create three Pods in that namespace:
- `frontend` with label `role=frontend` (image: `nginx`)
- `api` with label `role=api` (image: `nginx`)
- `db` with label `role=db` (image: `nginx`)

Create a NetworkPolicy named `api-policy` in namespace `network-test` that:
- Applies to Pods with label `role=api`
- Allows **ingress** only from Pods labeled `role=frontend` on TCP port 80
- Allows **egress** only to Pods labeled `role=db` on TCP port 5432
- Allows **DNS egress** (UDP port 53) to any namespace
- Denies all other ingress and egress traffic

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
