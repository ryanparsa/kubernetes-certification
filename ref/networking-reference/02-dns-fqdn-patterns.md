# Kubernetes Networking Reference — 2. DNS FQDN Patterns

> Part of [Kubernetes Networking Reference](../Networking Reference.md)


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

