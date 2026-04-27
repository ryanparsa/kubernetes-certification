# Kubernetes TLS and Identity: The Master Guide — 3. Certificate Distribution (5 Control Plane Nodes + Workers)

> Part of [Kubernetes TLS and Identity: The Master Guide](../TLS.md)


| Component | Cert Type | Distribution Strategy |
| --- | --- | --- |
| **Kubelet** | Client & Server | **Unique per Node** (Master or Worker) |
| **etcd** | Peer & Server | **Unique per Node** (For encrypted peering) |
| **API Server** | Server TLS | **Shared/Common** (Includes all Master IPs + Load Balancer) |
| **Scheduler** | Client TLS | **Shared** (Identity of the *role* matters, not the node) |
| **Controller Manager** | Client TLS | **Shared** (Identity of the *role* matters, not the node) |
| **Service Account (SA)** | Signing Keys | **Exactly Identical** (Must be copied to all masters) |

---

