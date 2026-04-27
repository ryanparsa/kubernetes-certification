# Kubernetes RBAC Reference

[← Back to index](../README.md)

---

## 9. Debugging RBAC Issues

```bash
# Find all RoleBindings for a ServiceAccount in a namespace
kubectl -n my-ns get rolebindings -o yaml | grep -A5 serviceaccount

# Find all ClusterRoleBindings for a user
kubectl get clusterrolebindings -o yaml | grep -B5 "name: jane"

# See what rules a Role has
kubectl -n my-ns describe role my-role

# Check which subjects have access to a resource
kubectl who-can get pods -n my-ns     # requires kubectl-who-can plugin
# or use:
kubectl get rolebindings,clusterrolebindings -A -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin")'

# Impersonate to test access (requires --as permission)
kubectl get pods --as system:serviceaccount:my-ns:my-sa -n my-ns
```

---
