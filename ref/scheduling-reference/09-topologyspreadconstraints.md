# Kubernetes Scheduling Reference — 9. TopologySpreadConstraints

> Part of [Kubernetes Scheduling Reference](../Scheduling Reference.md)


Spreads pods evenly across topology domains (nodes, zones).

```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1                          # max difference in pod count between domains
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: DoNotSchedule    # or ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
```

> `maxSkew: 1` means no domain can have more than 1 extra pod compared to the least-loaded domain.

---

