# Kubernetes RBAC Reference

[← Back to index](../README.md)

---

## 4. Imperative Commands

```bash
# Create ServiceAccount
kubectl -n project-hamster create sa processor

# Create Role
kubectl -n project-hamster create role processor \
  --verb=create \
  --resource=secret \
  --resource=configmap

# Create RoleBinding (SA format: namespace:name)
kubectl -n project-hamster create rolebinding processor \
  --role processor \
  --serviceaccount project-hamster:processor

# Create ClusterRole
kubectl create clusterrole pod-reader \
  --verb=get,list,watch \
  --resource=pods

# Create ClusterRoleBinding
kubectl create clusterrolebinding read-pods-global \
  --clusterrole=pod-reader \
  --user=jane

# Bind ClusterRole within a Namespace using RoleBinding
kubectl -n project-hamster create rolebinding read-pods \
  --clusterrole=pod-reader \
  --serviceaccount project-hamster:processor
```

---
