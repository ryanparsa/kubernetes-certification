# Kubernetes Networking Reference — 1. Services

> Part of [Kubernetes Networking Reference](../Networking Reference.md)


A Service is a stable virtual IP (ClusterIP) + DNS name that load-balances traffic to a
set of Pods selected by label.

### Service types

| Type | Cluster-internal? | External? | Use case |
|---|---|---|---|
| `ClusterIP` (default) | Yes | No | Internal communication only |
| `NodePort` | Yes | Via `NodeIP:NodePort` | Dev / simple external access |
| `LoadBalancer` | Yes | Via cloud LB | Production external access |
| `ExternalName` | Yes (CNAME) | Proxies to external DNS | Point to external service by name |
| Headless (`clusterIP: None`) | DNS only (no VIP) | No | StatefulSets, direct Pod DNS |

### ClusterIP

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: my-app
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80          # port the Service listens on
    targetPort: 8080  # port the Pod listens on
```

### NodePort

```yaml
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080   # optional; 30000-32767; auto-assigned if omitted
```

Access via any node: `http://NODE_IP:30080`

### LoadBalancer

```yaml
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
```

Provisions a cloud load balancer; external IP appears in `EXTERNAL-IP` column.

### ExternalName

```yaml
spec:
  type: ExternalName
  externalName: my-database.corp.example.com   # DNS CNAME target
```

No selector, no endpoints — DNS query returns a CNAME.

### Headless Service

```yaml
spec:
  clusterIP: None   # no VIP — DNS returns Pod IPs directly
  selector:
    app: my-statefulset
```

Used by StatefulSets so each pod gets a stable DNS name:
`pod-0.my-service.namespace.svc.cluster.local`

---

