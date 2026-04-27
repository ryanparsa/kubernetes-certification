# kubectl Output Formatting Reference

[← Back to index](../README.md)

---

## 3. `--sort-by`

`--sort-by` takes a JSONPath field expression. Applied to list output.

```bash
# Sort pods by creation time (oldest first)
kubectl get pod -A --sort-by=.metadata.creationTimestamp

# Sort pods by name
kubectl get pod -A --sort-by=.metadata.name

# Sort pods by uid
kubectl get pod -A --sort-by=.metadata.uid

# Sort nodes by memory capacity (descending not supported natively — pipe to sort)
kubectl get nodes --sort-by=.status.capacity.memory

# Sort events by last timestamp
kubectl get events -A --sort-by='.lastTimestamp'

# Sort PVs by capacity
kubectl get pv --sort-by=.spec.capacity.storage
```

---
