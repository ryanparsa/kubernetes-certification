## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Create the ClusterRole

```bash
kubectl create clusterrole pod-reader --verb=get,watch,list --resource=pods
```

Or using YAML:

```yaml
# lab/pod-reader-clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

```bash
kubectl apply -f lab/pod-reader-clusterrole.yaml
```

### Create the ClusterRoleBinding

```bash
kubectl create clusterrolebinding read-pods --clusterrole=pod-reader --user=jane
```

Or using YAML:

```yaml
# lab/read-pods-clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-pods
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f lab/read-pods-clusterrolebinding.yaml
```

### Verify

```bash
kubectl get clusterrole pod-reader
kubectl get clusterrolebinding read-pods
kubectl auth can-i list pods --as=jane
```

## Checklist (Score: 0/2)

- [ ] ClusterRole `pod-reader` exists with `get`, `watch`, and `list` permissions on `pods`
- [ ] ClusterRoleBinding `read-pods` binds ClusterRole `pod-reader` to user `jane`
