# kubectl Output Formatting Reference

[← Back to index](../README.md)

---

## 6. `jq` patterns

`jq` is available in most exam environments and is more powerful than JSONPath for
complex filtering.

```bash
# All pod names and their namespaces
kubectl get pods -A -o json | \
  jq '.items[] | {name:.metadata.name, ns:.metadata.namespace}'

# Pods not in Running state
kubectl get pods -A -o json | \
  jq '.items[] | select(.status.phase != "Running") | {name:.metadata.name, phase:.status.phase}'

# Container images used across the cluster
kubectl get pods -A -o json | \
  jq '[.items[].spec.containers[].image] | unique | sort[]'

# Nodes and their allocatable memory
kubectl get nodes -o json | \
  jq '.items[] | {node:.metadata.name, memory:.status.allocatable.memory}'

# Events sorted by last timestamp (jq sort)
kubectl get events -A -o json | \
  jq '[.items | sort_by(.lastTimestamp)[]] | .[] | {ns:.metadata.namespace, reason:.reason, msg:.message}'

# Find which ServiceAccounts have a given ClusterRoleBinding
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects[]'

# Count pods per node
kubectl get pods -A -o json | \
  jq '[.items[].spec.nodeName] | group_by(.) | map({node:.[0], count:length})'
```

---
