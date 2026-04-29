## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Create the namespace

```bash
kubectl create namespace cluster-admin
```

### Create ServiceAccount, Role, RoleBinding, and Pod

```yaml
# lab/rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-admin
  namespace: cluster-admin
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-admin
  namespace: cluster-admin
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["list", "get", "watch", "update"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["create", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-admin
  namespace: cluster-admin
subjects:
- kind: ServiceAccount
  name: app-admin
  namespace: cluster-admin
roleRef:
  kind: Role
  name: app-admin
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: v1
kind: Pod
metadata:
  name: admin-pod
  namespace: cluster-admin
spec:
  serviceAccountName: app-admin
  containers:
  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["sleep", "3600"]
```

```bash
kubectl apply -f lab/rbac.yaml
kubectl wait pod admin-pod -n cluster-admin --for=condition=Ready --timeout=60s
```

### Verify allowed and denied operations

```bash
# Allowed - list pods
kubectl exec -n cluster-admin admin-pod -- kubectl get pods -n cluster-admin

# Allowed - list deployments
kubectl exec -n cluster-admin admin-pod -- kubectl get deployments -n cluster-admin

# Denied - create pods (should fail)
kubectl auth can-i create pods -n cluster-admin --as=system:serviceaccount:cluster-admin:app-admin
```

## Checklist (Score: 7/7)

- [x] ServiceAccount `app-admin` exists in `cluster-admin` namespace
- [x] Role `app-admin` allows `list/get/watch` on `pods`
- [x] Role allows `list/get/watch/update` on `deployments`
- [x] Role allows `create/delete` on `configmaps`
- [x] RoleBinding `app-admin` binds the Role to the ServiceAccount
- [x] Pod `admin-pod` exists using `bitnami/kubectl:latest` with the ServiceAccount
- [x] Pod cannot create pods (RBAC enforced)
