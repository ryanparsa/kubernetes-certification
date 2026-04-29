## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Step 1: Create ClusterRole

```bash
kubectl create clusterrole app-reader --verb=get,list,watch --resource=pods,deployments
```

Or using a manifest:

```yaml
# lab/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: app-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]
```

### Step 2: Create ClusterRoleBinding

```bash
kubectl create clusterrolebinding app-reader --clusterrole=app-reader --serviceaccount=app:app-reader
```

Or using a manifest:

```yaml
# lab/clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: app-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: app-reader
subjects:
- kind: ServiceAccount
  name: app-reader
  namespace: app
```

### Step 3: Configure Kubeconfig Context

```bash
# Check current context to get cluster and user names
kubectl config get-contexts

# Create the new context
kubectl config set-context app-context \
  --cluster=kind-cka-lab-81 \
  --user=kind-cka-lab-81 \
  --namespace=app
```

## Checklist (Score: 3/3)

- [x] ClusterRole `app-reader` exists with `get`, `list`, `watch` on `pods` and `deployments`
- [x] ClusterRoleBinding `app-reader` binds `app-reader` ClusterRole to `app-reader` ServiceAccount in namespace `app`
- [x] Kubeconfig context `app-context` exists and uses namespace `app` by default
