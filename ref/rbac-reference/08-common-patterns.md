# Kubernetes RBAC Reference — 8. Common Patterns

> Part of [Kubernetes RBAC Reference](../RBAC Reference.md)


### Pattern 1 — Namespace-scoped read-only access for a ServiceAccount

```bash
kubectl create sa reader -n my-app
kubectl -n my-app create rolebinding reader \
  --clusterrole=view \
  --serviceaccount=my-app:reader
```

### Pattern 2 — Grant cross-namespace access (one SA reads pods in another NS)

```bash
# Allow SA in ns-a to list pods in ns-b
kubectl -n ns-b create rolebinding cross-ns-read \
  --clusterrole=view \
  --serviceaccount=ns-a:my-sa
```

### Pattern 3 — Minimal permissions (least privilege)

```yaml
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]           # no create/delete/update
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]                   # sub-resources listed separately
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["specific-secret"]  # restrict to a named resource
  verbs: ["get"]
```

### Pattern 4 — Operator / controller permissions

```yaml
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["events"]
  verbs: ["create", "patch"]
```

---

