## Answer

**Reference:** <https://kubernetes.io/docs/reference/access-authn-authz/rbac/>

### Create the Namespace and ServiceAccount

```bash
kubectl create namespace ci
kubectl create serviceaccount cicd-sa -n ci
```

### Create the Role

```bash
kubectl create role deployment-manager \
  --verb=create,update,delete \
  --resource=deployments \
  -n ci
```

Or using a manifest:

```yaml
# lab/deployment-manager-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: ci
rules:
- apiGroups:
  - apps
  resources:
  - deployments
  verbs:
  - create
  - update
  - delete
```

```bash
kubectl apply -f lab/deployment-manager-role.yaml
```

### Create the RoleBinding

```bash
kubectl create rolebinding cicd-sa-deployment-manager \
  --role=deployment-manager \
  --serviceaccount=ci:cicd-sa \
  -n ci
```

Or using a manifest:

```yaml
# lab/cicd-sa-deployment-manager.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cicd-sa-deployment-manager
  namespace: ci
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: deployment-manager
subjects:
- kind: ServiceAccount
  name: cicd-sa
  namespace: ci
```

```bash
kubectl apply -f lab/cicd-sa-deployment-manager.yaml
```

### Verify

```bash
# Should return "yes"
kubectl auth can-i create deployments \
  --as=system:serviceaccount:ci:cicd-sa \
  -n ci
# yes

# Should return "no"
kubectl auth can-i get pods \
  --as=system:serviceaccount:ci:cicd-sa \
  -n ci
# no
```

## Checklist (Score: 0/5)

- [ ] Namespace `ci` exists
- [ ] ServiceAccount `cicd-sa` exists in namespace `ci`
- [ ] Role `deployment-manager` exists in namespace `ci` with verbs `create`, `update`, `delete` on `deployments`
- [ ] RoleBinding `cicd-sa-deployment-manager` binds `deployment-manager` to `cicd-sa` in namespace `ci`
- [ ] `cicd-sa` can `create` deployments but cannot `get` pods in namespace `ci`
