# kubernetes Files

# Control Plane Node

```
/
├── usr/
│   ├── bin/
│   │   ├── kubelet                                              # The kubelet daemon binary
│   │   ├── kubectl                                              # CLI to interact with the cluster
│   │   └── kubeadm                                              # Bootstrap / upgrade tool for the cluster
│   └── local/
│       └── bin/                                                 # Alternative install location for the above binaries
├── opt/
│   └── cni/
│       └── bin/                                                 # CNI plugin executables (kindnet, bridge, host-local, etc.)
├── etc/
│   ├── kubernetes/                                              # Main k8s config root
│   │   ├── admin.conf                                           # kubeconfig for cluster admin (kubectl)
│   │   ├── controller-manager.conf                              # kubeconfig used by kube-controller-manager
│   │   ├── kubelet.conf                                         # kubeconfig used by kubelet to reach API server
│   │   ├── scheduler.conf                                       # kubeconfig used by kube-scheduler
│   │   ├── super-admin.conf                                     # kubeconfig with raw cluster-admin (bypasses RBAC)
│   │   ├── audit-policy.yaml                                    # (optional) defines which API requests to audit-log
│   │   ├── encryption-config.yaml                               # (optional) encryption-at-rest config for etcd secrets
│   │   ├── manifests/                                           # Static pod manifests — kubelet auto-starts these on boot
│   │   │   ├── etcd.yaml                                        # Static pod: etcd key-value store
│   │   │   ├── kube-apiserver.yaml                              # Static pod: API server (front door to the cluster)
│   │   │   ├── kube-controller-manager.yaml                     # Static pod: runs reconciliation control loops
│   │   │   └── kube-scheduler.yaml                              # Static pod: assigns pods to nodes
│   │   └── pki/                                                 # All TLS certs and keys for the control plane
│   │       ├── ca.crt                                           # Cluster root CA — signed everything below (public)
│   │       ├── ca.key                                           # Cluster root CA private key — most sensitive file
│   │       ├── apiserver.crt                                    # API server's TLS serving certificate
│   │       ├── apiserver.key                                    # API server's private key
│   │       ├── apiserver-etcd-client.crt                        # Cert: API server authenticates to etcd
│   │       ├── apiserver-etcd-client.key                        # Key for API server → etcd mTLS
│   │       ├── apiserver-kubelet-client.crt                     # Cert: API server authenticates to kubelet
│   │       ├── apiserver-kubelet-client.key                     # Key for API server → kubelet mTLS
│   │       ├── front-proxy-ca.crt                               # CA for the aggregation layer (extension API servers)
│   │       ├── front-proxy-ca.key                               # Private key for the front-proxy CA
│   │       ├── front-proxy-client.crt                           # Cert API server uses when proxying to aggregated APIs
│   │       ├── front-proxy-client.key                           # Key for front-proxy client auth
│   │       ├── sa.key                                           # Private key used to sign ServiceAccount JWT tokens kube-controller-manager
│   │       ├── sa.pub                                           # Public key used to verify ServiceAccount tokens kube-apiserver
│   │       └── etcd/                                            # etcd-specific TLS (separate CA from cluster)
│   │           ├── ca.crt                                       # etcd's own CA (independent of cluster CA)
│   │           ├── ca.key                                       # etcd CA private key
│   │           ├── server.crt                                   # etcd server's TLS serving certificate
│   │           ├── server.key                                   # etcd server's private key
│   │           ├── peer.crt                                     # Cert for etcd-to-etcd peer replication
│   │           ├── peer.key                                     # Key for etcd peer communication
│   │           ├── healthcheck-client.crt                       # Cert used by liveness probes to query etcd
│   │           └── healthcheck-client.key                       # Key for etcd health check client
│   ├── systemd/
│   │   └── system/
│   │       ├── kubelet.service                                   # Systemd unit that starts/restarts kubelet on boot
│   │       └── kubelet.service.d/
│   │           └── 10-kubeadm.conf                              # Drop-in that injects --config and extra flags into kubelet
│   ├── cni/
│   │   └── net.d/
│   │       └── 10-kindnet.conflist                              # CNI plugin config — defines the pod network (kindnet)
│   ├── containerd/
│   │   └── config.toml                                          # containerd daemon config (snapshotter, plugins, etc.)
│   └── crictl.yaml                                              # crictl CLI config — points to the containerd socket
├── run/
│   └── containerd/
│       └── containerd.sock                                      # Unix socket kubelet uses to talk to containerd (CRI)
└── var/
    ├── etcd/                                                    # etcd data directory — the entire cluster state lives here
    ├── log/
    │   ├── pods/                                                # Pod logs on disk, organized by namespace_name_uid/container/
    │   └── containers/                                          # Symlinks into /var/log/pods/ one per container
    └── lib/
        ├── cni/                                                 # CNI plugin runtime state and IPAM address allocations
        ├── containerd/                                          # Container image layers and snapshot storage
        └── kubelet/                                             # Kubelet's runtime state root
            ├── config.yaml                                      # Kubelet's own configuration (eviction, feature gates, etc.)
            ├── kubeadm-flags.env                                # Extra CLI flags injected into kubelet by kubeadm
            ├── cpu_manager_state                                # Persisted CPU manager policy state (for static pinning)
            ├── memory_manager_state                             # Persisted memory manager policy state
            ├── dra_manager_state                                # Dynamic Resource Allocation state (DRA feature gate)
            ├── checkpoints/                                     # Kubelet checkpoints for pod recovery across restarts
            ├── device-plugins/
            │   └── kubelet.sock                                 # Unix socket for device plugin API (GPUs, FPGAs, etc.)
            ├── pki/
            │   ├── kubelet-client-current.pem                   # Symlink → current rotated kubelet client cert+key
            │   ├── kubelet-client-<date>.pem                    # Actual rotated client cert kubelet uses to auth to API server
            │   ├── kubelet.crt                                  # Kubelet's serving cert (API server uses this to call kubelet)
            │   └── kubelet.key                                  # Kubelet's serving private key
            ├── plugins/                                         # CSI driver Unix socket directory
            ├── plugins_registry/                                # CSI plugin self-registration directory
            ├── pod-resources/
            │   └── kubelet.sock                                 # Socket exposing per-pod device/resource allocations
            └── pods/                                            # One subdirectory per running pod (named by UID)
                └── <pod-uid>/
                    ├── containers/                              # Per-container state (restart count, exit code, etc.)
                    ├── etc-hosts                                # The /etc/hosts file injected into this pod
                    ├── plugins/                                 # Pod-scoped plugin state (empty-dir readiness files)
                    └── volumes/                                 # Mounted volumes (projected tokens, configmaps, etc.)
                        ├── kubernetes.io~projected/
                        │   └── kube-api-access-<id>/
                        │       ├── token                        # Auto-rotated ServiceAccount JWT for this pod
                        │       ├── ca.crt                       # Cluster CA injected so the pod can verify the API server
                        │       └── namespace                    # The pod's namespace, available as a file
                        └── kubernetes.io~configmap/             # ConfigMap volumes mounted into the pod

```

# Worker node

```
/
├── usr/
│   └── bin/
│       └── kubelet                                              # The only required k8s binary on a worker
├── opt/
│   └── cni/
│       └── bin/                                                 # CNI plugin executables (bridge, host-local, kindnet, etc.)
├── etc/
│   ├── kubernetes/                                              # Much smaller than control plane — no PKI keys, no manifests
│   │   ├── kubelet.conf                                         # kubeconfig kubelet uses to authenticate to the API server
│   │   ├── manifests/                                           # Static pod manifests dir — empty on a worker node
│   │   └── pki/
│   │       └── ca.crt                                           # Cluster CA cert only — worker never holds any private keys
│   ├── systemd/
│   │   └── system/
│   │       ├── kubelet.service                                   # Systemd unit that starts/restarts kubelet on boot
│   │       └── kubelet.service.d/
│   │           └── 10-kubeadm.conf                              # Drop-in that injects --config and extra flags into kubelet
│   ├── cni/
│   │   └── net.d/
│   │       └── 10-kindnet.conflist                              # CNI plugin config — defines pod network on this node
│   ├── containerd/
│   │   └── config.toml                                          # containerd daemon config (snapshotter, plugins, etc.)
│   └── crictl.yaml                                              # crictl CLI config — points to the containerd socket
├── run/
│   └── containerd/
│       └── containerd.sock                                      # Unix socket kubelet uses to talk to containerd (CRI)
└── var/
    ├── log/
    │   ├── pods/                                                # Pod logs on disk, organized by namespace_name_uid/container/
    │   └── containers/                                          # Symlinks into /var/log/pods/, one per container
    └── lib/
        ├── cni/                                                 # CNI plugin runtime state and IPAM address allocations
        ├── containerd/                                          # Container image layers and snapshot storage
        └── kubelet/                                             # Kubelet's runtime state root
            ├── config.yaml                                      # Kubelet's runtime config (eviction thresholds, feature gates)
            ├── kubeadm-flags.env                                # Extra CLI flags injected into kubelet by kubeadm
            ├── cpu_manager_state                                # Persisted CPU manager policy state (for static pinning)
            ├── memory_manager_state                             # Persisted memory manager policy state
            ├── dra_manager_state                                # Dynamic Resource Allocation state (DRA feature gate)
            ├── checkpoints/                                     # Kubelet checkpoints for pod recovery across restarts
            ├── device-plugins/
            │   └── kubelet.sock                                 # Unix socket for device plugin API (GPUs, FPGAs, etc.)
            ├── pki/
            │   ├── kubelet-client-current.pem                   # Symlink → current rotated kubelet client cert+key
            │   ├── kubelet-client-<date>.pem                    # Actual rotated client cert kubelet uses to auth to API server
            │   ├── kubelet.crt                                  # Kubelet's serving cert (API server uses this to call kubelet)
            │   └── kubelet.key                                  # Kubelet's serving private key
            ├── plugins/                                         # CSI driver Unix socket directory
            ├── plugins_registry/                                # CSI plugin self-registration directory
            ├── pod-resources/
            │   └── kubelet.sock                                 # Socket exposing per-pod device/resource allocations
            └── pods/                                            # One subdirectory per running pod (named by UID)
                └── <pod-uid>/
                    ├── containers/                              # Per-container state (restart count, exit code, etc.)
                    ├── etc-hosts                                # The /etc/hosts file injected into this pod
                    ├── plugins/                                 # Pod-scoped plugin state (empty-dir readiness files)
                    └── volumes/                                 # Mounted volumes (projected tokens, configmaps, etc.)
                        ├── kubernetes.io~projected/
                        │   └── kube-api-access-<id>/
                        │       ├── token                        # Auto-rotated ServiceAccount JWT for this pod
                        │       ├── ca.crt                       # Cluster CA injected so the pod can verify the API server
                        │       └── namespace                    # The pod's namespace, available as a file
                        └── kubernetes.io~configmap/             # ConfigMap volumes mounted into the pod

```

# Kubernetes TLS and Identity: The Master Guide

This document serves as a technical reference for the distribution of certificates, roles, and identity management in a production-grade (HA) Kubernetes cluster.

---

## 1. The Core Concept: Server vs. Client

In Kubernetes TLS communication, every connection has two sides. Some components are "dual-role," meaning they act as both servers and clients depending on the direction of the request.

- **Server Role:** A component that listens on a port and presents a **Server TLS Certificate**.
- **Client Role:** A component that initiates a connection and presents a **Client TLS Certificate** (or token) for authentication.

---

## 2. Dual-Role Component Anatomy

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

## 3. Certificate Distribution (5 Control Plane Nodes + Workers)

| Component | Cert Type | Distribution Strategy |
| --- | --- | --- |
| **Kubelet** | Client & Server | **Unique per Node** (Master or Worker) |
| **etcd** | Peer & Server | **Unique per Node** (For encrypted peering) |
| **API Server** | Server TLS | **Shared/Common** (Includes all Master IPs + Load Balancer) |
| **Scheduler** | Client TLS | **Shared** (Identity of the *role* matters, not the node) |
| **Controller Manager** | Client TLS | **Shared** (Identity of the *role* matters, not the node) |
| **Service Account (SA)** | Signing Keys | **Exactly Identical** (Must be copied to all masters) |

---

## 4. Why Unique Certs for Kubelets? (Node Restriction)

The `NodeRestriction` Admission Controller prevents a compromised node from accessing data belonging to other nodes. This security is based on the **Common Name (CN)** inside each Kubelet's client certificate (e.g., `system:node:worker-1`).

> **Security Warning:** If Kubelet client certificates are shared across nodes, hacking one node effectively grants access to the data of all nodes sharing that identity.
> 

---

## 5. Non-TLS Keys in the PKI Directory

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
| `etcd/healthcheck-client.crt / key` | kubelet liveness probe | etcd health endpoint only (Least Privilege) |

---

## 6. Kubeconfig Files — Expiry and Renewal

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

## 7. Certificate Renewal Reference

### `/etc/kubernetes/pki/` — Control Plane Certs

| File | Expiry | Auto-renews? | How to renew |
|---|---|---|---|
| `ca.crt / ca.key` | **10 years** | No | Manual process (rare; requires re-issuing all signed certs) |
| `apiserver.crt` | 1 year | No | `kubeadm certs renew all` |
| `apiserver-etcd-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `apiserver-kubelet-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `front-proxy-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `etcd/ca.crt` | **10 years** | No | Manual process |
| `etcd/server.crt` | 1 year | No | `kubeadm certs renew all` |
| `etcd/peer.crt` | 1 year | No | `kubeadm certs renew all` |
| `etcd/healthcheck-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `sa.key / sa.pub` | **No expiry** | N/A | Not a certificate — no renewal needed |

### `/etc/kubernetes/` — Kubeconfig Files

| File | Expiry | Auto-renews? | How to renew |
|---|---|---|---|
| `kubelet.conf` | 1 year | **Yes** — Certificate Rotation (symlink swap, no restart) | Automatic |
| `admin.conf` | 1 year | No | `kubeadm certs renew all` + re-copy to workstation |
| `controller-manager.conf` | 1 year | No | `kubeadm certs renew all` + restart static pod |
| `scheduler.conf` | 1 year | No | `kubeadm certs renew all` + restart static pod |
| `super-admin.conf` | 1 year | No | `kubeadm certs renew all` |

### `/var/lib/kubelet/pki/` — Kubelet Node Certs

| File | Expiry | Auto-renews? | How to renew |
|---|---|---|---|
| `kubelet-client-<date>.pem` | 1 year | **Yes** — kubelet requests new cert, writes dated file | Automatic |
| `kubelet-client-current.pem` | (symlink) | **Yes** — symlink flipped atomically on rotation | Automatic |
| `kubelet.crt / kubelet.key` | 1 year | **No** by default | Requires `serverTLSBootstrap: true` in kubelet config to enable auto-rotation; otherwise manual |

> **After any `kubeadm certs renew all`:** restart kube-apiserver, kube-scheduler, kube-controller-manager static pods so they reload the new files. Re-copy `admin.conf` to any workstation `~/.kube/config`.

---

## 8. Architecture Summary

1. **Node Identity (Kubelet):** Always unique per machine.
2. **Role Identity (Scheduler/Controller):** Shared across Control Plane nodes.
3. **Chain of Trust (CA):** Identical across the entire cluster.
4. **Signing Keys (SA):** Must be manually synced to all Control Plane nodes.
5. **etcd CA:** Logically isolated from the main cluster CA.
6. **Kubeconfig certs:** 1-year validity — renew via upgrade or `kubeadm certs renew all`; re-copy any workstation copies after renewal.