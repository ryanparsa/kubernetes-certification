# Kubernetes Scheduling Reference — 11. Deployment on All Nodes

> Part of [Kubernetes Scheduling Reference](../Scheduling Reference.md)


A DaemonSet guarantees one-per-node. To run a Deployment on all nodes use:

```yaml
spec:
  replicas: <total node count>
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: my-app
            topologyKey: kubernetes.io/hostname
```

This prevents two replicas landing on the same node.

---

