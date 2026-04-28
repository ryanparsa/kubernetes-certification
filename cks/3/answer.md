## Answer

**Reference:** https://kubernetes.io/docs/concepts/security/pod-security-admission/

### Create the namespace with Pod Security Standard label

```bash
kubectl create namespace api-security
kubectl label namespace api-security pod-security.kubernetes.io/enforce=baseline
```

Or declaratively:

```yaml
# lab/api-security-ns.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: api-security
  labels:
    pod-security.kubernetes.io/enforce: baseline
```

### Create the compliant pod

```yaml
# lab/secure-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
  namespace: api-security
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
  containers:
  - name: nginx
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
```

```bash
kubectl apply -f lab/secure-pod.yaml
```

### Create the Role and RoleBinding for PSS viewing

```yaml
# lab/pss-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pss-viewer-role
  namespace: api-security
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get"]
- apiGroups: [""]
  resources: ["namespaces/status"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pss-viewer-binding
  namespace: api-security
subjects:
- kind: ServiceAccount
  name: pss-viewer
  namespace: api-security
roleRef:
  kind: Role
  name: pss-viewer-role
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f lab/pss-rbac.yaml
```

### Verify

```bash
kubectl get namespace api-security --show-labels
kubectl get pod secure-pod -n api-security
kubectl get role,rolebinding -n api-security
```

## Checklist (Score: 0/5)

- [ ] Namespace `api-security` exists with label `pod-security.kubernetes.io/enforce=baseline`
- [ ] Pod `secure-pod` exists in namespace `api-security`
- [ ] Pod `secure-pod` complies with baseline PSS (non-root, no privilege escalation)
- [ ] Role `pss-viewer-role` exists with namespace read permissions
- [ ] RoleBinding `pss-viewer-binding` binds role to ServiceAccount `pss-viewer`
