# kubectl Output Formatting Reference — 8. Practical One-Liners

> Part of [kubectl Output Formatting Reference](../kubectl Output Formatting.md)


```bash
# Write a script that lists all pods sorted by creationTimestamp
echo 'kubectl get pod -A --sort-by=.metadata.creationTimestamp' > find_pods.sh

# Write a script that lists all pods sorted by uid
echo 'kubectl get pod -A --sort-by=.metadata.uid' > find_pods_uid.sh

# Get all container images running in the cluster (unique, sorted)
kubectl get pods -A -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | \
  sort -u

# List all nodes with their OS image and kernel version
kubectl get nodes -o custom-columns=\
NAME:.metadata.name,\
OS:.status.nodeInfo.osImage,\
KERNEL:.status.nodeInfo.kernelVersion

# Check resource requests for all pods
kubectl get pods -A -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[0].resources.requests.cpu,\
MEM_REQ:.spec.containers[0].resources.requests.memory

# List PVs sorted by capacity
kubectl get pv --sort-by=.spec.capacity.storage \
  -o custom-columns=\
NAME:.metadata.name,\
CAPACITY:.spec.capacity.storage,\
POLICY:.spec.persistentVolumeReclaimPolicy,\
STATUS:.status.phase

# Get events for Warning type, sorted by time
kubectl get events -A \
  --field-selector type=Warning \
  --sort-by='.lastTimestamp' \
  -o custom-columns=\
NS:.metadata.namespace,\
TIME:.lastTimestamp,\
REASON:.reason,\
OBJ:.involvedObject.name
```

---

