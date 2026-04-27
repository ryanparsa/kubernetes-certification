# Useful Commands

```bash
# See why a pod is pending
kubectl describe pod my-pod | grep -A 10 Events

# List node labels
kubectl get nodes --show-labels
kubectl describe node worker-1 | grep Labels -A 20

# Check node allocatable resources vs requests
kubectl describe node worker-1 | grep -A 5 Allocatable

# Check which node a pod is on
kubectl get pod my-pod -o wide

# Cordon a node (prevent new pods)
kubectl cordon worker-1

# Drain a node (evict all pods + cordon)
kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data

# Uncordon a node
kubectl uncordon worker-1
```
