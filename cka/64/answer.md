## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the namespace

```bash
kubectl create namespace network
```

### Create Deployments, Services, and NetworkPolicies

```yaml
# lab/64-netpol.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: network
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: network
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: db
  namespace: network
spec:
  replicas: 1
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: postgres
        image: postgres
        env:
        - name: POSTGRES_HOST_AUTH_METHOD
          value: trust
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-policy
  namespace: network
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: api
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: network
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Egress
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: db
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
  namespace: network
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api
```

```bash
kubectl apply -f lab/64-netpol.yaml
kubectl wait deployment web api db -n network --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get networkpolicies -n network
kubectl get deployments -n network
```

## Checklist (Score: 0/7)

- [ ] Deployment `web` (nginx) exists in `network` namespace
- [ ] Deployment `api` (nginx) exists in `network` namespace
- [ ] Deployment `db` (postgres) exists in `network` namespace with `POSTGRES_HOST_AUTH_METHOD=trust`
- [ ] NetworkPolicy `web-policy` allows `web` egress only to `api`
- [ ] NetworkPolicy `api-policy` allows `api` ingress from `web` and egress only to `db`
- [ ] NetworkPolicy `db-policy` allows `db` ingress only from `api`
- [ ] All other inter-pod traffic is denied
