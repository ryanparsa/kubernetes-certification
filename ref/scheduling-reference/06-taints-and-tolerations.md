# Kubernetes Scheduling Reference — 6. Taints and Tolerations

> Part of [Kubernetes Scheduling Reference](../Scheduling Reference.md)


**Taints** repel pods from nodes. **Tolerations** allow pods to be scheduled despite a taint.

### Taint effects

| Effect | Meaning |
|---|---|
| `NoSchedule` | New pods without a matching toleration won't be scheduled |
| `PreferNoSchedule` | Scheduler tries to avoid placing pods here; not guaranteed |
| `NoExecute` | Existing pods without toleration are evicted; new pods also blocked |

### Managing taints

```bash
# Taint a node
kubectl taint node worker-1 gpu=true:NoSchedule

# Taint with NoExecute (evicts existing pods too)
kubectl taint node worker-1 maintenance=:NoExecute

# Remove a taint (append -)
kubectl taint node worker-1 gpu=true:NoSchedule-

# View taints on a node
kubectl describe node worker-1 | grep Taints
```

### Toleration in a Pod spec

```yaml
spec:
  tolerations:
  - key: gpu
    operator: Equal
    value: "true"
    effect: NoSchedule
  - key: node-role.kubernetes.io/control-plane
    operator: Exists            # matches any value
    effect: NoSchedule
  - key: maintenance
    operator: Exists
    effect: NoExecute
    tolerationSeconds: 300      # stay for 5min then evict
```

### Control plane taint

`kubeadm` adds `node-role.kubernetes.io/control-plane:NoSchedule` to control-plane
nodes. To schedule user workloads on the control plane, add a matching toleration or
remove the taint:

```bash
# Remove control-plane taint (single-node cluster)
kubectl taint node <node> node-role.kubernetes.io/control-plane:NoSchedule-
```

---

