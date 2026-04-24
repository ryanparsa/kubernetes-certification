# Kubernetes Networking Reference

Comprehensive reference for cluster networking: Services, DNS, NetworkPolicy, Ingress,
Gateway API, CoreDNS, kube-proxy, and Service CIDR management.

---

## 1. Services

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

## 2. DNS FQDN Patterns

CoreDNS resolves these names inside the cluster:

| Resource | FQDN pattern | Resolves to |
|---|---|---|
| Service | `SERVICE.NAMESPACE.svc.cluster.local` | ClusterIP (or Pod IPs for headless) |
| Headless Service Pod | `POD.SERVICE.NAMESPACE.svc.cluster.local` | Pod IP directly |
| Pod by IP | `a-b-c-d.NAMESPACE.pod.cluster.local` | Pod IP (dashes replace dots) |
| `kubernetes` API service | `kubernetes.default.svc.cluster.local` | API server ClusterIP |

> **Short names work too but are not FQDNs:**
> `SERVICE` (same namespace), `SERVICE.NAMESPACE` — avoid in configs that need reliability.

### Examples

```bash
# Service kubernetes in namespace default
kubernetes.default.svc.cluster.local

# Headless service department in namespace lima-workload
# (resolves to all pod IPs via DNS A records)
department.lima-workload.svc.cluster.local

# Specific pod section100 in headless service setup
section100.department.lima-workload.svc.cluster.local

# Pod with IP 1.2.3.4 in namespace kube-system
1-2-3-4.kube-system.pod.cluster.local
```

### Testing DNS inside a pod

```bash
# Run a temporary debug pod
kubectl run -it --rm dns-test --image=busybox:1.35 -- sh

# Inside the pod:
nslookup kubernetes.default.svc.cluster.local
nslookup my-service.my-ns.svc.cluster.local
cat /etc/resolv.conf
```

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

## 4. Ingress

Ingress routes external HTTP/HTTPS traffic to Services based on host and path rules.
Requires an Ingress Controller (nginx, traefik, etc.) to be installed.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: my-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
  tls:
  - hosts:
    - app.example.com
    secretName: tls-secret
```

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

## 6. CoreDNS

CoreDNS runs as a Deployment in `kube-system`, exposed via the `kube-dns` Service at
the cluster DNS IP (usually `10.96.0.10`).

```bash
# Find the DNS service IP
kubectl -n kube-system get svc kube-dns

# Check CoreDNS pods
kubectl -n kube-system get pods -l k8s-app=kube-dns

# View CoreDNS config
kubectl -n kube-system get configmap coredns -o yaml
```

### CoreDNS ConfigMap (Corefile)

```
.:53 {
    errors
    health {       lameduck 5s }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf {
       max_concurrent 1000
    }
    cache 30
    loop
    reload
    loadbalance
}
```

### Adding a custom upstream DNS (stub zone)

```
my-corp.internal:53 {
    errors
    cache 30
    forward . 192.168.1.1
}
```

Add the block to the Corefile in the ConfigMap and restart CoreDNS pods:

```bash
kubectl -n kube-system rollout restart deployment coredns
```

---

## 7. kube-proxy

kube-proxy runs as a DaemonSet on every node and implements Service VIP routing.

### Modes

| Mode | Mechanism | Notes |
|---|---|---|
| `iptables` (default) | iptables DNAT rules | Stable, random load-balancing |
| `ipvs` | Linux IPVS | Better performance at scale, more LB algorithms |
| `nftables` | nftables (Kubernetes 1.29+) | Modern replacement for iptables mode |

```bash
# Check current mode
kubectl -n kube-system get configmap kube-proxy -o yaml | grep mode

# Inspect iptables rules for a Service
iptables-save | grep <service-cluster-ip>

# Inspect IPVS virtual servers (if IPVS mode)
ipvsadm -Ln
```

---

## 8. Service CIDR Change Procedure

Changing the Service CIDR after cluster creation requires updating multiple components.

### Steps (kubeadm cluster)

```bash
# 1. Update kube-apiserver static pod manifest
vim /etc/kubernetes/manifests/kube-apiserver.yaml
# Change: --service-cluster-ip-range=NEW_CIDR

# 2. Update kube-controller-manager static pod manifest
vim /etc/kubernetes/manifests/kube-controller-manager.yaml
# Change: --service-cluster-ip-range=NEW_CIDR

# 3. Update kube-proxy configmap
kubectl -n kube-system edit configmap kube-proxy
# Change clusterCIDR or the iptables/ipvs config

# 4. Update CoreDNS Service (kube-dns) IP if needed
# Delete the kube-dns Service so it gets a new IP from the new CIDR
kubectl -n kube-system delete svc kube-dns
# Re-create it with an explicit IP from the new CIDR:
kubectl -n kube-system expose deployment coredns \
  --name=kube-dns \
  --port=53 \
  --protocol=UDP \
  --cluster-ip=NEW_DNS_IP

# 5. Update kubelet's clusterDNS setting on each node
# Edit /var/lib/kubelet/config.yaml:
# clusterDNS:
# - NEW_DNS_IP
# Then restart kubelet: systemctl restart kubelet

# 6. Restart affected pods so they pick up the new /etc/resolv.conf
# Recreate kube-proxy DaemonSet pods
kubectl -n kube-system rollout restart daemonset kube-proxy
```

> All existing Services retain their old ClusterIPs until deleted and re-created.
> The `kubernetes` Service in the `default` Namespace must also be deleted and re-created.

---

## 9. Useful Commands

```bash
# List all Services with ClusterIP and ports
kubectl get svc -A

# Describe a Service (see Endpoints)
kubectl describe svc my-service -n my-app

# Check endpoints for a Service
kubectl get endpoints my-service -n my-app

# Test connectivity from a debug pod
kubectl run -it --rm test --image=busybox:1.35 -- \
  wget -qO- http://my-service.my-app.svc.cluster.local

# List NetworkPolicies
kubectl get networkpolicies -A

# Describe a NetworkPolicy
kubectl describe networkpolicy np-backend -n project-snake

# Check which pods match a NetworkPolicy selector
kubectl -n my-app get pods -l app=backend
```
