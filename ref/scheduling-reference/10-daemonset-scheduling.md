# Kubernetes Scheduling Reference — 10. DaemonSet Scheduling

> Part of [Kubernetes Scheduling Reference](../Scheduling Reference.md)


A DaemonSet ensures exactly one pod per node (or per matching node). It bypasses the
default scheduler for node placement — it uses its own controller.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane   # run on control-plane too
        operator: Exists
        effect: NoSchedule
      nodeSelector:
        kubernetes.io/os: linux       # optional: limit to Linux nodes
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16
```

DaemonSet pods on tainted nodes (e.g. control-plane) require matching tolerations.

---

