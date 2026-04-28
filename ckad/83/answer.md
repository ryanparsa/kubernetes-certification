## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the namespace and seed Pods

```bash
kubectl create namespace network-test
kubectl run frontend --image=nginx -n network-test -l role=frontend
kubectl run api --image=nginx -n network-test -l role=api
kubectl run db --image=nginx -n network-test -l role=db
```

### Create the NetworkPolicy

```yaml
# lab/api-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: network-test
spec:
  podSelector:
    matchLabels:
      role: api
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
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: db
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
```

```bash
kubectl apply -f lab/api-policy.yaml
```

### Verify

```bash
kubectl get networkpolicy api-policy -n network-test
kubectl describe networkpolicy api-policy -n network-test
```

### Key points

- Both `policyTypes: [Ingress, Egress]` are required — omitting one causes those rules to be silently ignored.
- The DNS egress rule (`namespaceSelector: {}`) must be present or service-name resolution will break.
- All other ingress and egress traffic is implicitly denied once a NetworkPolicy selects the Pod.

## Checklist (Score: 0/3)

- [ ] NetworkPolicy `api-policy` exists in namespace `network-test` and targets Pods with label `role=api`
- [ ] Ingress is allowed only from Pods labeled `role=frontend` on TCP port 80
- [ ] Egress is allowed only to Pods labeled `role=db` on TCP 5432, plus DNS (UDP 53) to any namespace
