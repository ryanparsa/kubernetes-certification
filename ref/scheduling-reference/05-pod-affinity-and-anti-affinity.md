# Kubernetes Scheduling Reference — 5. Pod Affinity and Anti-Affinity

> Part of [Kubernetes Scheduling Reference](../Scheduling Reference.md)


Schedules pods relative to **other pods** (co-location or spread).

### Pod Affinity — place with matching pods

```yaml
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: cache          # schedule near pods with app=cache
        topologyKey: kubernetes.io/hostname
```

### Pod Anti-Affinity — avoid nodes with matching pods

```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: frontend       # don't schedule on same node as other frontend pods
        topologyKey: kubernetes.io/hostname
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: frontend
          topologyKey: topology.kubernetes.io/zone    # spread across zones
```

> `topologyKey` groups nodes by a label. Common values:
> - `kubernetes.io/hostname` — node-level
> - `topology.kubernetes.io/zone` — availability zone
> - `topology.kubernetes.io/region` — region

---

