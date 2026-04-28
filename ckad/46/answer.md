## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the namespace

```bash
kubectl create namespace networking
```

### Create pods and NetworkPolicy

```yaml
# lab/46.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: networking
---
apiVersion: v1
kind: Pod
metadata:
  name: secure-db
  namespace: networking
  labels:
    app: db
spec:
  containers:
  - name: postgres
    image: postgres:12
    env:
    - name: POSTGRES_PASSWORD
      value: password
---
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: networking
  labels:
    role: frontend
spec:
  containers:
  - name: nginx
    image: nginx
---
apiVersion: v1
kind: Pod
metadata:
  name: monitoring
  namespace: networking
  labels:
    role: monitoring
spec:
  containers:
  - name: nginx
    image: nginx
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-network-policy
  namespace: networking
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 5432
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: monitoring
    ports:
    - protocol: TCP
      port: 8080
```

```bash
kubectl apply -f lab/46.yaml
```

### Verify

```bash
kubectl get pods -n networking
kubectl get networkpolicy -n networking
kubectl describe networkpolicy db-network-policy -n networking
```

## Checklist (Score: 0/5)

- [ ] Namespace `networking` exists
- [ ] All three pods (`secure-db`, `frontend`, `monitoring`) are created correctly
- [ ] NetworkPolicy `db-network-policy` exists and targets pods with label `app=db`
- [ ] NetworkPolicy allows ingress only from pods with `role=frontend` on port `5432`
- [ ] NetworkPolicy allows egress only to pods with `role=monitoring` on port `8080`
