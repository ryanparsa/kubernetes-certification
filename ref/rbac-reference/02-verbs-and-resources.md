# Kubernetes RBAC Reference — 2. Verbs and Resources

> Part of [Kubernetes RBAC Reference](../RBAC Reference.md)


### All standard verbs

| Verb | HTTP method | Meaning |
|---|---|---|
| `get` | GET single | Read one resource |
| `list` | GET collection | List all resources of a type |
| `watch` | GET (watch stream) | Stream change events |
| `create` | POST | Create a resource |
| `update` | PUT | Replace the whole resource |
| `patch` | PATCH | Partial update |
| `delete` | DELETE single | Delete one resource |
| `deletecollection` | DELETE collection | Delete all matching resources |
| `use` | — | Special: use a PodSecurityPolicy or StorageClass |
| `bind` | — | Special: bind a Role/ClusterRole (used by RoleBindings) |
| `escalate` | — | Special: allow granting permissions the subject doesn't hold |
| `impersonate` | — | Special: act as another user/group/SA |
| `*` | — | Wildcard — all verbs |

### Common API groups

| API Group | String in YAML | Covers |
|---|---|---|
| Core (v1) | `""` (empty string) | Pods, Services, Secrets, ConfigMaps, Nodes, PVs, PVCs, Namespaces, ServiceAccounts |
| apps | `apps` | Deployments, StatefulSets, DaemonSets, ReplicaSets |
| batch | `batch` | Jobs, CronJobs |
| autoscaling | `autoscaling` | HorizontalPodAutoscalers |
| networking | `networking.k8s.io` | Ingresses, NetworkPolicies |
| gateway | `gateway.networking.k8s.io` | Gateways, HTTPRoutes |
| rbac | `rbac.authorization.k8s.io` | Roles, ClusterRoles, RoleBindings, ClusterRoleBindings |
| storage | `storage.k8s.io` | StorageClasses, VolumeAttachments |
| policy | `policy` | PodDisruptionBudgets |
| `*` | `*` | All groups |

---

