# Kubernetes TLS and Identity: The Master Guide — 2. Dual-Role Component Anatomy

> Part of [Kubernetes TLS and Identity: The Master Guide](../TLS.md)


### A) kube-apiserver

- **As a Server:** The central hub for all components (Port 6443).
- **As a Client (to etcd):** Needs a client cert to read/write data to the database.
- **As a Client (to Kubelet):** Needs a client cert to enter a node for `kubectl logs` or `exec`.

### B) kubelet (`/var/lib/kubelet/pki/`)

**As a Client** — reports pod status, watches for assignments:

| File | Description |
|---|---|
| `kubelet-client-<date>.pem` | The actual rotated client cert+key. A new dated file is issued automatically before the old one expires. |
| `kubelet-client-current.pem` | **Symlink** pointing to the latest dated file above. kubelet always reads this path — when a new cert is issued, only the symlink target is updated. This is how Certificate Rotation works **without a restart**. |

**As a Server** — listens on Port 10250 for `kubectl logs`, `exec`, etc.:

| File | Description |
|---|---|
| `kubelet.crt` | Serving certificate kubelet presents to the API Server to prove it's the real kubelet on this node. |
| `kubelet.key` | Private key for the serving cert. |

---

