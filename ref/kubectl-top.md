# `kubectl top` — Resource Usage

`kubectl top` shows live CPU and memory consumption from **metrics-server**. If
metrics-server is not installed the command fails with `Metrics API not available`.

```bash
# Node resource usage
kubectl top node

# Example output:
# NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# master     192m         9%     1234Mi           65%
# worker-1   88m          4%     891Mi            47%

# Pod resource usage (current namespace)
kubectl top pod

# All namespaces
kubectl top pod -A

# Specific namespace
kubectl top pod -n kube-system

# Show containers individually within each pod
kubectl top pod -A --containers

# Sort by CPU (highest first) — pipe to sort; --sort-by not supported for top
kubectl top pod -A --no-headers | sort -k3 -rn | head -10

# Sort by memory
kubectl top pod -A --no-headers | sort -k4 -rn | head -10

# Find highest CPU node
kubectl top node --no-headers | sort -k2 -rn | head -1

# Find highest memory node
kubectl top node --no-headers | sort -k4 -rn | head -1
```

### Checking if metrics-server is available

```bash
# metrics-server runs as a Deployment in kube-system
kubectl -n kube-system get deployment metrics-server

# Verify the Metrics API is registered
kubectl api-resources | grep metrics

# If missing, check the API service
kubectl get apiservice v1beta1.metrics.k8s.io -o yaml
```

### Common `kubectl top` fields

| Field | `kubectl top node` | `kubectl top pod` |
|---|---|---|
| `CPU(cores)` | millicores used by all processes | millicores used by all containers |
| `CPU%` | % of node allocatable CPU | — |
| `MEMORY(bytes)` | working set memory | working set memory |
| `MEMORY%` | % of node allocatable memory | — |

> `kubectl top` reflects the **current instant** (a scrape from metrics-server).
> For trends and history, use Prometheus + Grafana or `kubectl describe node` for
> resource request/limit totals.

---

