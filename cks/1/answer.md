## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the NetworkPolicy

```yaml
# lab/secure-backend.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-backend
  namespace: network-security
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - port: 5432
```

```bash
kubectl apply -f lab/secure-backend.yaml
```

### Verify

```bash
kubectl get networkpolicy secure-backend -n network-security
kubectl describe networkpolicy secure-backend -n network-security
```

The policy should show:
- **Ingress:** allows traffic from `app=frontend` pods on port 8080
- **Egress:** allows traffic to `app=database` pods on port 5432

## Checklist (Score: 0/5)

- [ ] NetworkPolicy `secure-backend` exists in namespace `network-security`
- [ ] NetworkPolicy selects pods with label `app=backend`
- [ ] NetworkPolicy has correct ingress rule (from `app=frontend` on port 8080)
- [ ] NetworkPolicy has correct egress rule (to `app=database` on port 5432)
- [ ] Both Ingress and Egress policyTypes are specified
