# Core Objects

| Object | Scope | Purpose |
|---|---|---|
| `Role` | Namespace | Defines permissions *within* a single Namespace |
| `ClusterRole` | Cluster-wide | Defines permissions across the whole cluster, or for non-namespaced resources |
| `RoleBinding` | Namespace | Grants a Role or ClusterRole to subjects *within* a single Namespace |
| `ClusterRoleBinding` | Cluster-wide | Grants a ClusterRole to subjects *across the whole cluster* |

### The 4 RBAC combinations

| Role type | Binding type | Effect |
|---|---|---|
| `Role` | `RoleBinding` | Permissions in one Namespace only |
| `ClusterRole` | `ClusterRoleBinding` | Permissions cluster-wide |
| `ClusterRole` | `RoleBinding` | ClusterRole reused, but applied in one Namespace only |
| `Role` | `ClusterRoleBinding` | **Not possible** — a namespaced Role cannot be applied cluster-wide |

> Use `ClusterRole` + `RoleBinding` to avoid duplicating the same Role definition across many Namespaces.

---

