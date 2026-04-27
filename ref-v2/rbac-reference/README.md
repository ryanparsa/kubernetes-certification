# Kubernetes RBAC Reference

[← Back to index](../README.md)

# Kubernetes RBAC Reference

RBAC (Role-Based Access Control) is the authorisation mechanism that controls what a
subject (user, group, ServiceAccount) is allowed to do in the cluster. Every API request
goes through: Authentication → Authorisation (RBAC) → Admission Control.

---

## Sections

- [1. Core Objects](01-core-objects.md)
- [2. Verbs and Resources](02-verbs-and-resources.md)
- [3. YAML Examples](03-yaml-examples.md)
- [4. Imperative Commands](04-imperative-commands.md)
- [5. ServiceAccount → RBAC → Pod Token Flow](05-serviceaccount-rbac-pod-token-flow.md)
- [6. `kubectl auth can-i`](06-kubectl-auth-can-i.md)
- [7. Built-in ClusterRoles](07-built-in-clusterroles.md)
- [8. Common Patterns](08-common-patterns.md)
- [9. Debugging RBAC Issues](09-debugging-rbac-issues.md)
- [10. Quick Reference](10-quick-reference.md)
