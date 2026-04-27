# Kubernetes Scheduling Reference

[← Back to index](../README.md)

---

## 4. Node Affinity

More expressive than `nodeSelector`. Supports `In`, `NotIn`, `Exists`, `DoesNotExist`,
`Gt`, `Lt` operators.

### Required (hard rule — pod not scheduled if not met)

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
            - nvme
```

### Preferred (soft rule — scheduler tries but doesn't guarantee)

```yaml
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 80                    # higher weight = stronger preference (1-100)
        preference:
          matchExpressions:
          - key: region
            operator: In
            values:
            - us-east-1
      - weight: 20
        preference:
          matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
```

> `IgnoredDuringExecution` — already-running pods are NOT evicted if the node labels change.

---
