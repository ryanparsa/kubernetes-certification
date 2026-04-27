# Kubernetes TLS and Identity: The Master Guide

[← Back to index](../README.md)

---

## 8. Architecture Summary

1. **Node Identity (Kubelet):** Always unique per machine.
2. **Role Identity (Scheduler/Controller):** Shared across Control Plane nodes.
3. **Chain of Trust (CA):** Identical across the entire cluster.
4. **Signing Keys (SA):** Must be manually synced to all Control Plane nodes.
5. **etcd CA:** Logically isolated from the main cluster CA.
6. **Kubeconfig certs:** 1-year validity — renew via upgrade or `kubeadm certs renew all`; re-copy any workstation copies after renewal.
