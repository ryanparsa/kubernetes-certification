# Question 69

> **Solve this question on:** `cka-lab-69`

Create three *Pods* in the `default` namespace, each exposed via a *ClusterIP* service on port `80`:

| Pod name   | Image | Service name   |
|------------|-------|----------------|
| `consumer` | nginx | `consumer`     |
| `producer` | nginx | `producer`     |
| `web`      | nginx | `web`          |

Create a *NetworkPolicy* named `limit-consumer` that:

- Selects the `consumer` pod.
- Allows **ingress** traffic **only** from pods labelled `run=producer`.
- Denies ingress from all other pods (including `web`).

Verify that `producer` can reach `consumer` and `web` cannot.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
