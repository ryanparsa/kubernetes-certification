# Question 76

> **Solve this question on:** `ckad-lab-76`

The namespace `app-stack` contains three *Pods*: `frontend` (label `tier=frontend`), `backend` (label `tier=backend`), and `database` (label `tier=database`). All three *Pods* carry the label `app=todo`.

Create a *NetworkPolicy* named `app-stack-network-policy` in the `app-stack` namespace that:

- Targets the `database` *Pod* (matched by labels `app=todo, tier=database`).
- Allows **ingress** traffic only from the `backend` *Pod* (matched by labels `app=todo, tier=backend`).
- Restricts allowed traffic to **TCP port 3306** only.
- Implicitly **denies** ingress from the `frontend` *Pod* and any other source.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
