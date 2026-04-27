# Kubernetes Workloads Reference — 1. Pod QoS Classes

> Part of [Kubernetes Workloads Reference](../Workloads Reference.md)


Kubernetes assigns a QoS class to each pod based on resource requests and limits.
This determines eviction order when a node is under memory pressure.

### QoS classes

| Class | Condition | Eviction priority |
|---|---|---|
| `Guaranteed` | Every container has equal `requests` and `limits` for CPU and memory | Last to be evicted |
| `Burstable` | At least one container has a request or limit set, but not Guaranteed | Middle |
| `BestEffort` | No container has any requests or limits | First to be evicted |

### Examples

```yaml
# Guaranteed — requests == limits for ALL containers
resources:
  requests:
    cpu: "500m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

```yaml
# Burstable — requests set but not matching limits
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

```yaml
# BestEffort — nothing set
resources: {}
```

```bash
# Check QoS class
kubectl get pod my-pod -o jsonpath='{.status.qosClass}'

# List pods sorted by QoS (BestEffort first)
kubectl get pods -A -o custom-columns=\
NAME:.metadata.name,QOS:.status.qosClass,NS:.metadata.namespace
```

> Pods in the `Guaranteed` class also get dedicated CPU (no throttling) when the CPU
> manager policy is set to `static`.

---

