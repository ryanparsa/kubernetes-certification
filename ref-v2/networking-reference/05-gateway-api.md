# Kubernetes Networking Reference

[← Back to index](../README.md)

---

## 5. Gateway API

The Gateway API (gateway.networking.k8s.io) is the successor to Ingress, with richer
semantics and role separation.

| Object | Role |
|---|---|
| `GatewayClass` | Defines which controller handles gateways (cluster-scoped) |
| `Gateway` | Represents a load balancer / listener config |
| `HTTPRoute` | Defines routing rules (namespace-scoped) |

```yaml
# Gateway
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
  namespace: my-app
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same

---
# HTTPRoute
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-route
  namespace: my-app
spec:
  parentRefs:
  - name: my-gateway
  hostnames:
  - "app.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: api-service
      port: 80
```

### Ingress vs Gateway API

| Feature | Ingress | Gateway API |
|---|---|---|
| API version | `networking.k8s.io/v1` | `gateway.networking.k8s.io/v1` |
| Role separation | Single object | GatewayClass / Gateway / Route |
| Traffic types | HTTP/HTTPS only | HTTP, TCP, TLS, gRPC |
| Status | Stable, widely used | GA since Kubernetes 1.28 |
| Cross-namespace routing | No | Yes (via allowedRoutes) |

---
