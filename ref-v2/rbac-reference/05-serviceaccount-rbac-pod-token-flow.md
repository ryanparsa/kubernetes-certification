# Kubernetes RBAC Reference

[← Back to index](../README.md)

---

## 5. ServiceAccount → RBAC → Pod Token Flow

```
1. Pod is created with spec.serviceAccountName: processor
2. kubelet mounts a projected volume into the pod at:
     /var/run/secrets/kubernetes.io/serviceaccount/token   ← auto-rotated JWT
     /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  ← cluster CA
     /var/run/secrets/kubernetes.io/serviceaccount/namespace
3. Pod reads the token and calls the API server:
     curl https://kubernetes.default.svc/api/v1/namespaces/... \
       -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
4. API server validates the token (verifies JWT signature using sa.pub)
5. API server checks RBAC: does ServiceAccount processor have permission?
6. Access granted or denied
```

> Tokens are projected (not stored as Secrets) and auto-rotated by default (1h lifetime, kubelet refreshes before expiry).

### Using a custom token (legacy)

```yaml
# Force a non-expiring Secret-based token (avoid in modern clusters)
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: processor-token
  namespace: project-hamster
  annotations:
    kubernetes.io/service-account.name: processor
```

---
