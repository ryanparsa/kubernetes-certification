# Kubernetes Troubleshooting Reference

[← Back to index](../README.md)

---

## 9. Common Troubleshooting Commands

```bash
# Find all non-Running pods cluster-wide
kubectl get pods -A --field-selector 'status.phase!=Running'

# Find pods with high restart counts
kubectl get pods -A | awk '$5 > 5'   # 5th column is RESTARTS

# Describe any resource to see events
kubectl describe <resource> <name> -n <ns>

# Check available resources on all nodes
kubectl describe nodes | grep -A 5 "Allocated resources"

# Tail kubelet logs in real time
journalctl -u kubelet -f

# Check container runtime status
systemctl status containerd
crictl ps -a
crictl logs <container-id>

# List images on a node
crictl images

# Remove unused images
crictl rmi --prune
```
