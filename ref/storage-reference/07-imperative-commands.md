# Kubernetes Storage Reference — 7. Imperative Commands

> Part of [Kubernetes Storage Reference](../Storage Reference.md)


```bash
# Create a PVC
kubectl -n my-app create -f pvc.yaml

# List PVs and PVCs
kubectl get pv
kubectl get pvc -A

# Describe a PV (see events)
kubectl describe pv safari-pv

# Delete a PVC (PV behaviour depends on reclaimPolicy)
kubectl delete pvc safari-pvc -n project-t230

# Manually reclaim a Released PV (Retain policy)
# 1. Delete the PV
kubectl delete pv safari-pv
# 2. Clean up the storage manually
# 3. Re-create the PV
```

---

