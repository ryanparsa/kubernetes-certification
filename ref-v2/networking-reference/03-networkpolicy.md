# Kubernetes Networking Reference

[← Back to index](../README.md)

---

## 3. NetworkPolicy

Without NetworkPolicies all pod-to-pod traffic is allowed. Once a NetworkPolicy selects
a pod, **only explicitly allowed traffic is permitted** for the matched policy types.

### Key concepts

- `podSelector`: which pods this policy applies to (empty = all pods in namespace)
- `policyTypes`: `Ingress`, `Egress`, or both
- If `Ingress` in `policyTypes` but no `ingress:` rules → all ingress is denied
- If `Egress` in `policyTypes` but no `egress:` rules → all egress is denied
- Multiple rules in a list are OR-ed together
- Within a single rule, `from`/`to` + `ports` conditions are AND-ed together

### Ingress policy example

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
  namespace: my-app
spec:
  podSelector:
    matchLabels:
      app: backend           # applies to backend pods
  policyTypes:
    - Ingress
  ingress:
  - from:                    # condition: source selector
    - podSelector:
        matchLabels:
          app: frontend
    ports:                   # condition: port
    - protocol: TCP
      port: 8080
```

### Egress policy example (correct multi-target)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: np-backend
  namespace: project-snake
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
  -                          # rule 1: backend → db1:1111
    to:
    - podSelector:
        matchLabels:
          app: db1
    ports:
    - protocol: TCP
      port: 1111
  -                          # rule 2: backend → db2:2222
    to:
    - podSelector:
        matchLabels:
          app: db2
    ports:
    - protocol: TCP
      port: 2222
```

Reads as: allow egress if **(to=db1 AND port=1111) OR (to=db2 AND port=2222)**

### ⚠️ Common mistake — wrong AND/OR

```yaml
# WRONG — this means: (to=db1 OR to=db2) AND (port=1111 OR port=2222)
# Allows backend→db2:1111 which should be forbidden
egress:
- to:
  - podSelector:
      matchLabels:
        app: db1
  - podSelector:
      matchLabels:
        app: db2
  ports:
  - port: 1111
  - port: 2222
```

### NamespaceSelector

```yaml
from:
- namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: monitoring   # allow from entire namespace
- podSelector:
    matchLabels:
      app: prometheus
```

> `namespaceSelector` and `podSelector` in the same list item → AND (same pod in that namespace)
> In separate list items → OR (either condition grants access)

### Allow all egress to a CIDR (e.g. for DNS)

```yaml
egress:
- to:
  - ipBlock:
      cidr: 0.0.0.0/0
      except:
      - 10.0.0.0/8
```

### Allow DNS (required when blocking all egress)

```yaml
egress:
- ports:
  - port: 53
    protocol: UDP
  - port: 53
    protocol: TCP
```

---
