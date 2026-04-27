# Kubernetes TLS and Identity: The Master Guide — 6. Kubeconfig Files — Expiry and Renewal

> Part of [Kubernetes TLS and Identity: The Master Guide](../TLS.md)


Kubeconfig files embed mTLS certificates with a **1-year default validity** (kubeadm default).

### Auto-renewing
- **`kubelet.conf`** — kubelet has built-in **Certificate Rotation**: requests a new cert from the API Server before expiry, writes it as a new dated `.pem` file in `/var/lib/kubelet/pki/`, then atomically flips the `kubelet-client-current.pem` symlink to point at it — no restart needed.

### Do NOT auto-renew
- `admin.conf`, `controller-manager.conf`, `scheduler.conf` — expire silently after 365 days.

**Consequences of expiry:** Controller Manager and Scheduler stop talking to API Server; `kubectl` returns `Unauthorized`.

### Renewal options

**Option 1 — Cluster upgrade (recommended):** `kubeadm upgrade` regenerates all kubeconfig certs automatically.

**Option 2 — Manual:**
```
kubeadm certs renew all
```
Then restart Control Plane static pods so they reload the new files.

### admin.conf vs super-admin.conf

Both are human-admin kubeconfigs. `kubeadm certs renew` updates only the originals in `/etc/kubernetes/` — **copies on workstations are never updated automatically**.

After every renewal, re-copy manually:
```
scp master:/etc/kubernetes/admin.conf ~/.kube/config
```

| | `admin.conf` | `super-admin.conf` |
|---|---|---|
| **Purpose** | Day-to-day admin work | Break-glass / emergency recovery |
| **Privilege** | `system:masters` | Bypasses RBAC entirely |
| **Where to keep** | Can be copied to workstations | Master node only — never copy off |

> `super-admin.conf` available from Kubernetes 1.29+. Use only when RBAC misconfiguration locks out all admin access.

---

