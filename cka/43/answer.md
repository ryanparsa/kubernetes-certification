## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the namespace

```bash
kubectl create namespace networking
```

### Create the NetworkPolicy

```yaml
# lab/db-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
  namespace: networking
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 3306
```

```bash
kubectl apply -f lab/db-policy.yaml
```

### Verify

```bash
kubectl get networkpolicy db-policy -n networking
kubectl describe networkpolicy db-policy -n networking
```

## Checklist (Score: 0/5)

- [ ] NetworkPolicy `db-policy` exists in namespace `networking`
- [ ] Policy applies to pods with label `role=db`
- [ ] Policy type is `Ingress`
- [ ] Ingress is allowed from pods with label `role=frontend`
- [ ] Ingress is allowed only on port `3306`
