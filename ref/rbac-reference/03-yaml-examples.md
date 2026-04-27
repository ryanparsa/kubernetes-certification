# Kubernetes RBAC Reference — 3. YAML Examples

> Part of [Kubernetes RBAC Reference](../RBAC Reference.md)


### Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: processor
  namespace: project-hamster
rules:
- apiGroups:
  - ""                    # core group: Secrets, ConfigMaps, Pods, etc.
  resources:
  - secrets
  - configmaps
  verbs:
  - create
```

### ClusterRole

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

### RoleBinding (to a ServiceAccount)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: processor
  namespace: project-hamster
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: processor
subjects:
- kind: ServiceAccount
  name: processor
  namespace: project-hamster
```

### ClusterRoleBinding (to a User)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
```

### RoleBinding to a Group

```yaml
subjects:
- kind: Group
  name: system:masters
  apiGroup: rbac.authorization.k8s.io
```

---

