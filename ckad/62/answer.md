## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/#networkpolicy-resource

### Create the namespace and pods

```bash
kubectl create namespace netpol-namespace
kubectl run web-pod --image=nginx --port=80 --labels="tier=web" -n netpol-namespace
kubectl run app-pod --image=nginx --port=80 --labels="tier=app" -n netpol-namespace
kubectl run db-pod  --image=nginx --port=80 --labels="tier=db"  -n netpol-namespace
kubectl wait pod/web-pod pod/app-pod pod/db-pod -n netpol-namespace --for=condition=Ready --timeout=60s
```

### Apply default-deny policy

```yaml
# lab/62-default-deny.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: netpol-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

```bash
kubectl apply -f lab/62-default-deny.yaml
```

### Apply web -> app NetworkPolicies

```yaml
# lab/62-netpol.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-policy
  namespace: netpol-namespace
spec:
  podSelector:
    matchLabels:
      tier: web
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: app
    ports:
    - port: 80
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-policy
  namespace: netpol-namespace
spec:
  podSelector:
    matchLabels:
      tier: app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: web
    ports:
    - port: 80
```

```bash
kubectl apply -f lab/62-netpol.yaml
```

### Verify

```bash
kubectl get networkpolicy -n netpol-namespace
kubectl describe networkpolicy web-policy -n netpol-namespace
kubectl describe networkpolicy app-policy -n netpol-namespace
```

## Checklist (Score: 0/5)

- [ ] Namespace `netpol-namespace` exists with pods `web-pod`, `app-pod`, and `db-pod` running
- [ ] Default-deny NetworkPolicy blocks all ingress and egress by default
- [ ] NetworkPolicy `web-policy` allows egress from `tier=web` to `tier=app` on port `80` only
- [ ] NetworkPolicy `app-policy` allows ingress to `tier=app` from `tier=web` on port `80` only
- [ ] `web-pod` cannot directly reach `db-pod`
