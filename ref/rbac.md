# Kubernetes RBAC Reference

RBAC (Role-Based Access Control) is the authorisation mechanism that controls what a
subject (user, group, ServiceAccount) is allowed to do in the cluster. Every API request
goes through: Authentication -> Authorisation (RBAC) -> Admission Control.

---

## 1. Core Objects

| Object | Scope | Purpose |
|---|---|---|
| `Role` | Namespace | Defines permissions *within* a single Namespace |
| `ClusterRole` | Cluster-wide | Defines permissions across the whole cluster, or for non-namespaced resources |
| `RoleBinding` | Namespace | Grants a Role or ClusterRole to subjects *within* a single Namespace |
| `ClusterRoleBinding` | Cluster-wide | Grants a ClusterRole to subjects *across the whole cluster* |

### The 4 RBAC combinations

| Role type | Binding type | Effect |
|---|---|---|
| `Role` | `RoleBinding` | Permissions in one Namespace only |
| `ClusterRole` | `ClusterRoleBinding` | Permissions cluster-wide |
| `ClusterRole` | `RoleBinding` | ClusterRole reused, but applied in one Namespace only |
| `Role` | `ClusterRoleBinding` | **Not possible** - a namespaced Role cannot be applied cluster-wide |

> Use `ClusterRole` + `RoleBinding` to avoid duplicating the same Role definition across many Namespaces.

---

## 2. Verbs and Resources

### All standard verbs

| Verb | HTTP method | Meaning |
|---|---|---|
| `get` | GET single | Read one resource |
| `list` | GET collection | List all resources of a type |
| `watch` | GET (watch stream) | Stream change events |
| `create` | POST | Create a resource |
| `update` | PUT | Replace the whole resource |
| `patch` | PATCH | Partial update |
| `delete` | DELETE single | Delete one resource |
| `deletecollection` | DELETE collection | Delete all matching resources |
| `use` | - | Special: use a PodSecurityPolicy or StorageClass |
| `bind` | - | Special: bind a Role/ClusterRole (used by RoleBindings) |
| `escalate` | - | Special: allow granting permissions the subject doesn't hold |
| `impersonate` | - | Special: act as another user/group/SA |
| `*` | - | Wildcard - all verbs |

### Common API groups

| API Group | String in YAML | Covers |
|---|---|---|
| Core (v1) | `""` (empty string) | Pods, Services, Secrets, ConfigMaps, Nodes, PVs, PVCs, Namespaces, ServiceAccounts |
| apps | `apps` | Deployments, StatefulSets, DaemonSets, ReplicaSets |
| batch | `batch` | Jobs, CronJobs |
| autoscaling | `autoscaling` | HorizontalPodAutoscalers |
| networking | `networking.k8s.io` | Ingresses, NetworkPolicies |
| gateway | `gateway.networking.k8s.io` | Gateways, HTTPRoutes |
| rbac | `rbac.authorization.k8s.io` | Roles, ClusterRoles, RoleBindings, ClusterRoleBindings |
| storage | `storage.k8s.io` | StorageClasses, VolumeAttachments |
| policy | `policy` | PodDisruptionBudgets |
| `*` | `*` | All groups |

---

## 3. YAML Examples

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

## 4. Imperative Commands

```bash
# Create ServiceAccount
kubectl -n project-hamster create sa processor

# Create Role
kubectl -n project-hamster create role processor \
  --verb=create \
  --resource=secret \
  --resource=configmap

# Create RoleBinding (SA format: namespace:name)
kubectl -n project-hamster create rolebinding processor \
  --role processor \
  --serviceaccount project-hamster:processor

# Create ClusterRole
kubectl create clusterrole pod-reader \
  --verb=get,list,watch \
  --resource=pods

# Create ClusterRoleBinding
kubectl create clusterrolebinding read-pods-global \
  --clusterrole=pod-reader \
  --user=jane

# Bind ClusterRole within a Namespace using RoleBinding
kubectl -n project-hamster create rolebinding read-pods \
  --clusterrole=pod-reader \
  --serviceaccount project-hamster:processor
```

---

## 5. ServiceAccount -> RBAC -> Pod Token Flow

```
1. Pod is created with spec.serviceAccountName: processor
2. kubelet mounts a projected volume into the pod at:
     /var/run/secrets/kubernetes.io/serviceaccount/token   <- auto-rotated JWT
     /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  <- cluster CA
     /var/run/secrets/kubernetes.io/serviceaccount/namespace
3. Pod reads the token and calls the API server:
     curl https://kubernetes.default.svc/api/v1/namespaces/... \
       -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
4. API server validates the token (verifies JWT signature using sa.pub)
5. API server checks RBAC: does ServiceAccount processor have permission?
6. Access granted or denied
```

> Tokens are projected (not stored as Secrets) and auto-rotated by default (1h lifetime, kubelet refreshes before expiry).

### Using a custom token (legacy)

```yaml
# Force a non-expiring Secret-based token (avoid in modern clusters)
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: processor-token
  namespace: project-hamster
  annotations:
    kubernetes.io/service-account.name: processor
```

---

## 6. `kubectl auth can-i`

```bash
# Can the current user create pods?
kubectl auth can-i create pods

# Can a ServiceAccount create secrets in a namespace?
kubectl -n project-hamster auth can-i create secret \
  --as system:serviceaccount:project-hamster:processor
# Output: yes

# Can a ServiceAccount delete configmaps?
kubectl -n project-hamster auth can-i delete configmap \
  --as system:serviceaccount:project-hamster:processor
# Output: no

# List all actions available to the current user in a namespace
kubectl -n project-hamster auth can-i --list

# List all actions for a ServiceAccount
kubectl -n project-hamster auth can-i --list \
  --as system:serviceaccount:project-hamster:processor

# Check as a User (for kubeconfig-based users)
kubectl auth can-i get nodes --as jane
```

---

## 7. Built-in ClusterRoles

| ClusterRole | Grants |
|---|---|
| `cluster-admin` | Full access to everything - all verbs on all resources |
| `admin` | Full namespace access except ResourceQuota and Namespace itself |
| `edit` | Read/write to most namespaced resources; no RBAC management |
| `view` | Read-only to most namespaced resources; no Secrets |
| `system:node` | Used by kubelets - access to pods and node objects |
| `system:kube-scheduler` | Permissions the scheduler needs |
| `system:kube-controller-manager` | Permissions the controller manager needs |

```bash
# Inspect a built-in ClusterRole
kubectl describe clusterrole view
kubectl get clusterrole cluster-admin -o yaml
```

---

## 8. Common Patterns

### Pattern 1 - Namespace-scoped read-only access for a ServiceAccount

```bash
kubectl create sa reader -n my-app
kubectl -n my-app create rolebinding reader \
  --clusterrole=view \
  --serviceaccount=my-app:reader
```

### Pattern 2 - Grant cross-namespace access (one SA reads pods in another NS)

```bash
# Allow SA in ns-a to list pods in ns-b
kubectl -n ns-b create rolebinding cross-ns-read \
  --clusterrole=view \
  --serviceaccount=ns-a:my-sa
```

### Pattern 3 - Minimal permissions (least privilege)

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

### Pattern 4 - Operator / controller permissions

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

## 9. Debugging RBAC Issues

```bash
# Find all RoleBindings for a ServiceAccount in a namespace
kubectl -n my-ns get rolebindings -o yaml | grep -A5 serviceaccount

# Find all ClusterRoleBindings for a user
kubectl get clusterrolebindings -o yaml | grep -B5 "name: jane"

# See what rules a Role has
kubectl -n my-ns describe role my-role

# Check which subjects have access to a resource
kubectl who-can get pods -n my-ns     # requires kubectl-who-can plugin
# or use:
kubectl get rolebindings,clusterrolebindings -A -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin")'

# Impersonate to test access (requires --as permission)
kubectl get pods --as system:serviceaccount:my-ns:my-sa -n my-ns
```

---

## 10. Quick Reference

| Subject format for `--as` | Example |
|---|---|
| User | `jane` |
| ServiceAccount | `system:serviceaccount:NAMESPACE:NAME` |
| Group | `system:masters` |

| `subjects[].kind` values in YAML | |
|---|---|
| `User` | Human user authenticated via kubeconfig |
| `Group` | Group of users (e.g. `system:authenticated`) |
| `ServiceAccount` | Pod identity; `namespace` field required |
