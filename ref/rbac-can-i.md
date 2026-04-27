# `kubectl auth can-i`

```bash
# Can the current user create pods?
kubectl auth can-i create pods

# Can a ServiceAccount create secrets in a namespace?
kubectl -n project-hamster auth can-i create secret \
  --as system:serviceaccount:project-hamster:processor
# Output: yes

# Can a ServiceAccount delete configmaps?
kubectl -n project-hamster auth can-i delete configmap \
  --as system:serviceaccount:project-hamster:processor
# Output: no

# List all actions available to the current user in a namespace
kubectl -n project-hamster auth can-i --list

# List all actions for a ServiceAccount
kubectl -n project-hamster auth can-i --list \
  --as system:serviceaccount:project-hamster:processor

# Check as a User (for kubeconfig-based users)
kubectl auth can-i get nodes --as jane
```

---

