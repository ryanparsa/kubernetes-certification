## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the namespace (if not present)

```bash
kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
```

### Create the NetworkPolicy

```yaml
# lab/allow-traffic.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-traffic
  namespace: networking
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 80
```

```bash
kubectl apply -f lab/allow-traffic.yaml
```

### Verify

```bash
kubectl get networkpolicy allow-traffic -n networking
kubectl describe networkpolicy allow-traffic -n networking
```

## Checklist (Score: 0/3)

- [ ] NetworkPolicy `allow-traffic` exists in namespace `networking`
- [ ] NetworkPolicy selects pods with label `app=web`
- [ ] NetworkPolicy allows ingress only from pods with label `tier=frontend` on TCP port `80`
