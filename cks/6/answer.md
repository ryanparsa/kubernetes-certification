## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Create the namespace and ServiceAccount

```bash
kubectl create namespace rbac-minimize
kubectl create serviceaccount app-reader -n rbac-minimize
```

### Create the Role with minimal permissions

```yaml
# lab/app-reader-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader-role
  namespace: rbac-minimize
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "watch", "list"]
```

### Create the RoleBinding

```yaml
# lab/app-reader-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-reader-binding
  namespace: rbac-minimize
subjects:
- kind: ServiceAccount
  name: app-reader
  namespace: rbac-minimize
roleRef:
  kind: Role
  name: app-reader-role
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f lab/app-reader-role.yaml
kubectl apply -f lab/app-reader-binding.yaml
```

### Verify

```bash
kubectl get role app-reader-role -n rbac-minimize -o yaml
kubectl get rolebinding app-reader-binding -n rbac-minimize -o yaml

# Check that secrets are NOT accessible
kubectl auth can-i get secrets -n rbac-minimize --as=system:serviceaccount:rbac-minimize:app-reader
# should output: no

# Check pods ARE accessible
kubectl auth can-i get pods -n rbac-minimize --as=system:serviceaccount:rbac-minimize:app-reader
# should output: yes
```

## Checklist (Score: 0/5)

- [ ] Role `app-reader-role` exists in namespace `rbac-minimize`
- [ ] Role grants `get`, `watch`, `list` on `pods` and `services` (core API group)
- [ ] Role grants `get`, `watch`, `list` on `deployments` (`apps` API group)
- [ ] Role does NOT grant access to `secrets` or `configmaps`
- [ ] RoleBinding `app-reader-binding` binds `app-reader-role` to ServiceAccount `app-reader`
