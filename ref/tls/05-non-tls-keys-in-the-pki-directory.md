# Kubernetes TLS and Identity: The Master Guide — 5. Non-TLS Keys in the PKI Directory

> Part of [Kubernetes TLS and Identity: The Master Guide](../TLS.md)


Some files in `/etc/kubernetes/pki` are not used for TLS handshakes but are vital for identity:

- **Encryption Config:** An AES key (often stored in a separate YAML) used to encrypt sensitive Secrets at rest inside etcd.

### sa.key / sa.pub — ServiceAccount Token Signing

Unlike every other file in `/etc/kubernetes/pki`, these are **not TLS certificates** — they are a plain RSA key pair used to sign and verify ServiceAccount JWT tokens.

| File | Holder | Role |
|---|---|---|
| `sa.key` (private) | `kube-controller-manager` | **Signs** JWT tokens and injects them into new pods |
| `sa.pub` (public) | `kube-apiserver` | **Verifies** that incoming tokens were signed by the controller |

Flow: pod starts → controller signs a token with `sa.key` → pod presents token to API Server → API Server validates signature with `sa.pub` → access granted.

> In HA clusters, `sa.key` and `sa.pub` must be **identical copies** on all Control Plane nodes — if they differ, tokens signed on one master will be rejected by API Servers on other masters.

### front-proxy-ca / front-proxy-client — API Aggregation

These files support **API Aggregation**: extending the Kubernetes API with external API servers (e.g., `metrics-server` for `kubectl top`).

**How it works:**
1. `kubectl top pods` hits the main API Server.
2. Main API Server recognizes the request belongs to an aggregated API and proxies it to the extension server.
3. The extension server verifies the request truly came from the trusted API Server (not a spoofed caller).

| File | Purpose |
|---|---|
| `front-proxy-ca.crt/key` | CA that signs the front-proxy client cert; extension servers trust this CA |
| `front-proxy-client.crt/key` | Client cert the main API Server presents when proxying to extension servers |

**Impact if expired/deleted:** `kubectl top` and any aggregated APIs stop working.

### etcd PKI — Isolated Certificate Authority

etcd has its own CA (`etcd/ca.crt`) separate from the main cluster CA. Security isolation: even if the main CA were compromised, an attacker still couldn't connect directly to etcd.

**3 communication layers:**

| File pair | Used by | Talks to |
|---|---|---|
| `etcd/ca.crt / ca.key` | etcd CA | Signs all etcd certs below |
| `etcd/server.crt / server.key` | etcd server | Presented to `kube-apiserver` (only authorized client) |
| `etcd/peer.crt / peer.key` | etcd nodes | Each other — Raft replication in HA clusters |
| `etcd/healthcheck-client.crt / key` | etcd pod liveness probe | etcd health endpoint only (Least Privilege) |

---

