# PriorityClass

Determines the scheduling order and eviction priority for pods.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000            # higher number = higher priority
globalDefault: false
preemptionPolicy: PreemptLowerPriority   # default
description: "Critical workloads"
```

```yaml
spec:
  priorityClassName: high-priority
  containers:
  - name: app
    image: nginx
```

Built-in classes:
- `system-cluster-critical` (2000000000) — used by CoreDNS, kube-dns
- `system-node-critical` (2000001000) — used by kube-proxy, metrics-server

---

