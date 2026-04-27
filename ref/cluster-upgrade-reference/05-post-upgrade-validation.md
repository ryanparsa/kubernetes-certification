# Kubernetes Cluster Upgrade Reference — 5. Post-Upgrade Validation

> Part of [Kubernetes Cluster Upgrade Reference](../Cluster Upgrade Reference.md)


```bash
# All nodes should show the new version and be Ready
kubectl get nodes
# NAME              STATUS   ROLES           AGE   VERSION
# control-plane     Ready    control-plane   10d   v1.30.0
# worker-1          Ready    <none>          10d   v1.30.0

# Verify system pods are running
kubectl -n kube-system get pods

# Check component versions
kubectl version --short

# Run a quick smoke test
kubectl run smoke --image=nginx --restart=Never
kubectl get pod smoke
kubectl delete pod smoke
```

---

