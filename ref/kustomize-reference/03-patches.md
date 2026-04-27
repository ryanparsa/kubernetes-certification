# Kustomize Reference — 3. Patches

> Part of [Kustomize Reference](../Kustomize Reference.md)


Two patch formats are supported:

### Strategic Merge Patch

Looks like a partial Kubernetes resource. Kubernetes merges it using strategic merge rules
(lists are merged by name/key, not replaced wholesale).

```yaml
# replica-patch.yaml (strategic merge patch)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway          # must match the target resource
spec:
  replicas: 4                # overrides the base value
  template:
    spec:
      containers:
      - name: httpd
        resources:
          requests:
            cpu: 200m
```

Reference in `kustomization.yaml`:

```yaml
patches:
  - path: replica-patch.yaml
```

### JSON6902 Patch (RFC 6902)

Precise, operation-based. Useful when strategic merge doesn't work (e.g. removing array elements).

Operations: `add`, `remove`, `replace`, `move`, `copy`, `test`

```yaml
# json6902-patch.yaml
- op: replace
  path: /spec/replicas
  value: 6
- op: add
  path: /spec/template/spec/containers/0/env/-
  value:
    name: ENV
    value: production
- op: remove
  path: /spec/template/spec/containers/0/resources
```

Reference in `kustomization.yaml`:

```yaml
patches:
  - target:
      kind: Deployment
      name: api-gateway
    path: json6902-patch.yaml
```

Or inline:

```yaml
patches:
  - target:
      kind: Deployment
      name: api-gateway
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 6
```

### Strategic Merge vs JSON6902

| | Strategic Merge | JSON6902 |
|---|---|---|
| Format | Partial resource YAML | Operations list |
| List handling | Smart (merge by key) | Replace entire list by default |
| Removing fields | Tricky — use `$patch: delete` | Clean: `op: remove` |
| Cross-kind patches | No | Yes (target specifies kind/name) |
| Readability | High | Lower |
| Use case | Field overrides, replica counts, image tags | Precise array manipulation, deletions |

---

