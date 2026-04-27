# Kubernetes TLS and Identity: The Master Guide

[← Back to index](../README.md)

# Kubernetes TLS and Identity: The Master Guide

This document serves as a technical reference for the distribution of certificates, roles, and identity management in a production-grade (HA) Kubernetes cluster.

---

## Sections

- [1. The Core Concept: Server vs. Client](01-the-core-concept-server-vs-client.md)
- [2. Dual-Role Component Anatomy](02-dual-role-component-anatomy.md)
- [3. Certificate Distribution (5 Control Plane Nodes + Workers)](03-certificate-distribution-5-control-plane-nodes-workers.md)
- [4. Why Unique Certs for Kubelets? (Node Restriction)](04-why-unique-certs-for-kubelets-node-restriction.md)
- [5. Non-TLS Keys in the PKI Directory](05-non-tls-keys-in-the-pki-directory.md)
- [6. Kubeconfig Files — Expiry and Renewal](06-kubeconfig-files-expiry-and-renewal.md)
- [7. Certificate Renewal Reference](07-certificate-renewal-reference.md)
- [9. Diagnostic Commands](08-diagnostic-commands.md)
- [8. Architecture Summary](09-architecture-summary.md)
