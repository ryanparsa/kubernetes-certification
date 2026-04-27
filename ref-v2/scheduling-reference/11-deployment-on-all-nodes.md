# Kubernetes Scheduling Reference

[← Back to index](../README.md)

---

## 11. Deployment on All Nodes

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
