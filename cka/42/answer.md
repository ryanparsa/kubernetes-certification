## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Create the ServiceAccount

```bash
kubectl create serviceaccount app-sa -n default
```

### Create the Role

```yaml
# lab/pod-reader.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

```bash
kubectl apply -f lab/pod-reader.yaml
```

### Create the RoleBinding

```yaml
# lab/read-pods.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f lab/read-pods.yaml
```

### Verify

```bash
kubectl auth can-i list pods --as=system:serviceaccount:default:app-sa -n default
```

## Checklist (Score: 0/7)

- [ ] ServiceAccount `app-sa` exists in namespace `default`
- [ ] Role `pod-reader` exists in namespace `default`
- [ ] Role allows verb `get` on `pods`
- [ ] Role allows verb `list` on `pods`
- [ ] RoleBinding `read-pods` exists in namespace `default`
- [ ] RoleBinding binds Role `pod-reader` to ServiceAccount `app-sa`
- [ ] ServiceAccount can list pods in `default` namespace
