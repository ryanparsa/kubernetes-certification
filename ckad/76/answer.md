## Answer

**Reference:** <https://kubernetes.io/docs/concepts/services-networking/network-policies/>

### Create the namespace and seed pods

```bash
kubectl create namespace app-stack

kubectl apply -f - <<'EOF'
kind: Pod
apiVersion: v1
metadata:
  name: frontend
  namespace: app-stack
  labels:
    app: todo
    tier: frontend
spec:
  containers:
  - name: frontend
    image: nginx
---
kind: Pod
apiVersion: v1
metadata:
  name: backend
  namespace: app-stack
  labels:
    app: todo
    tier: backend
spec:
  containers:
  - name: backend
    image: nginx
---
kind: Pod
apiVersion: v1
metadata:
  name: database
  namespace: app-stack
  labels:
    app: todo
    tier: database
spec:
  containers:
  - name: database
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: example
EOF
```

### Create the NetworkPolicy

```yaml
# lab/app-stack-network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-stack-network-policy
  namespace: app-stack
spec:
  podSelector:
    matchLabels:
      app: todo
      tier: database
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: todo
          tier: backend
    ports:
    - protocol: TCP
      port: 3306
```

```bash
kubectl apply -f lab/app-stack-network-policy.yaml
kubectl get networkpolicy -n app-stack
```

### Verify

```bash
kubectl get networkpolicy app-stack-network-policy -n app-stack
# NAME                       POD-SELECTOR             AGE
# app-stack-network-policy   app=todo,tier=database   5s
```

## Checklist (Score: 0/5)

- [ ] Namespace `app-stack` exists
- [ ] Pods `frontend`, `backend`, and `database` are running in `app-stack`
- [ ] *NetworkPolicy* `app-stack-network-policy` exists in `app-stack`
- [ ] Policy targets pods with labels `app=todo, tier=database`
- [ ] Policy allows ingress from `tier=backend` on TCP port 3306 only
