# Hints — Task 5

## Hint 1
Default-deny is a `NetworkPolicy` with empty `podSelector: {}` and `policyTypes: [Ingress]`
but no `ingress` rules.

## Solution

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: web
spec:
  podSelector: {}
  policyTypes: [Ingress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: web
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 8080
```

Apply with `kubectl apply -f -` (heredoc) or save to a file.
