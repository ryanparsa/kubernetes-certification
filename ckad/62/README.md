# Question 62

> **Solve this question on:** `ckad-lab-62`

Create a namespace called `netpol-namespace`.

Create three pods in that namespace:
- `web-pod` using `nginx` image with label `tier=web`
- `app-pod` using `nginx` image with label `tier=app`
- `db-pod` using `nginx` image with label `tier=db`

Create a default-deny NetworkPolicy for all ingress and egress in the namespace.

Create NetworkPolicies so that:
1. `web-pod` can only egress to `app-pod` on port `80`
2. `app-pod` allows ingress only from `web-pod` on port `80`

`web-pod` must not be able to reach `db-pod` directly.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
