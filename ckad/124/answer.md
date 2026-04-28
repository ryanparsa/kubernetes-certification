## Answer

**Reference:** <https://kubernetes.io/docs/reference/access-authn-authz/rbac/>

### Create the ServiceAccount

```bash
kubectl create serviceaccount secret-manager -n sun
```

### Create the ClusterRoleBinding

```bash
kubectl create clusterrolebinding secret-manager \
  --clusterrole=secret-manager \
  --serviceaccount=sun:secret-manager
```

### Verify permissions

```bash
# Should return: yes
kubectl auth can-i get secrets -n sun --as=system:serviceaccount:sun:secret-manager

# Should return: no
kubectl auth can-i get secrets -n moon --as=system:serviceaccount:sun:secret-manager
```

## Checklist (Score: 0/4)

- [ ] ServiceAccount `secret-manager` exists in Namespace `sun`
- [ ] ClusterRoleBinding `secret-manager` binds ServiceAccount to ClusterRole `secret-manager`
- [ ] ServiceAccount can `get` Secrets in Namespace `sun`
- [ ] ServiceAccount cannot `get` Secrets in Namespace `moon`
