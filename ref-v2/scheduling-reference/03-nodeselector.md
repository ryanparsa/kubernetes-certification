# Kubernetes Scheduling Reference

[← Back to index](../README.md)

---

## 3. nodeSelector

Simplest affinity mechanism. Pod is only scheduled on nodes whose labels match ALL
key/value pairs.

```yaml
spec:
  nodeSelector:
    disktype: ssd
    kubernetes.io/os: linux
  containers:
  - name: app
    image: nginx
```

```bash
# Label a node
kubectl label node worker-1 disktype=ssd

# Remove a label
kubectl label node worker-1 disktype-
```

---
