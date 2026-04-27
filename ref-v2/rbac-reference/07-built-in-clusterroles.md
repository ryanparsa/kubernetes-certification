# Kubernetes RBAC Reference

[← Back to index](../README.md)

---

## 7. Built-in ClusterRoles

| ClusterRole | Grants |
|---|---|
| `cluster-admin` | Full access to everything — all verbs on all resources |
| `admin` | Full namespace access except ResourceQuota and Namespace itself |
| `edit` | Read/write to most namespaced resources; no RBAC management |
| `view` | Read-only to most namespaced resources; no Secrets |
| `system:node` | Used by kubelets — access to pods and node objects |
| `system:kube-scheduler` | Permissions the scheduler needs |
| `system:kube-controller-manager` | Permissions the controller manager needs |

```bash
# Inspect a built-in ClusterRole
kubectl describe clusterrole view
kubectl get clusterrole cluster-admin -o yaml
```

---
