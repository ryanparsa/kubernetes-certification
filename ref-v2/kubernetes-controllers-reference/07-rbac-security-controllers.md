# Kubernetes Controllers Reference

[← Back to index](../README.md)

---

## RBAC & Security Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **ClusterRoleAggregation** | `pkg/controller/clusterroleaggregation/clusterroleaggregation_controller.go` | `ClusterRoleAggregationController` · `syncClusterRole()` merges rules from matching ClusterRoles into aggregate roles (e.g. `admin` includes `edit` and `view`) |
| **ServiceAccount** | `pkg/controller/serviceaccount/serviceaccounts_controller.go` | `ServiceAccountsController` · `syncServiceAccount()` creates the `default` ServiceAccount in every new Namespace |
| **Certificates** | `pkg/controller/certificates/` | `CertificateController` · `approver/` handles auto-approval, `signer/` handles signing of well-known CSR types (Node client certs, kubelet serving certs) |

---
