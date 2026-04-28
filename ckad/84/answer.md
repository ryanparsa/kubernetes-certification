## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Create the namespace and ServiceAccount

```bash
kubectl create namespace dev
kubectl create serviceaccount developer -n dev
```

### Create the Role

```bash
kubectl create role pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n dev
```

### Create the RoleBinding

```bash
kubectl create rolebinding developer-read-pods \
  --role=pod-reader \
  --serviceaccount=dev:developer \
  -n dev
```

### Verify

```bash
kubectl auth can-i list pods -n dev --as=system:serviceaccount:dev:developer
# Output: yes

kubectl auth can-i delete pods -n dev --as=system:serviceaccount:dev:developer
# Output: no
```

### Alternative — YAML approach

```yaml
# lab/pod-reader.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: dev
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-read-pods
  namespace: dev
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-reader
subjects:
- kind: ServiceAccount
  name: developer
  namespace: dev
```

```bash
kubectl apply -f lab/pod-reader.yaml
```

## Checklist (Score: 0/3)

- [ ] ServiceAccount `developer` exists in namespace `dev`
- [ ] Role `pod-reader` in namespace `dev` grants `get`, `list`, `watch` on Pods
- [ ] RoleBinding `developer-read-pods` binds `pod-reader` to ServiceAccount `developer`; `kubectl auth can-i list pods` returns `yes`
