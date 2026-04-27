# Kubernetes Storage Reference — 8. Quick Reference

> Part of [Kubernetes Storage Reference](../Storage Reference.md)


| PVC not binding? | Check |
|---|---|
| Wrong storageClassName | Both PV and PVC must have identical `storageClassName` |
| Insufficient capacity | PV size must be ≥ PVC request |
| Access mode mismatch | PV must include all access modes in PVC |
| PV already bound | Each PV can only bind to one PVC |
| Selector mismatch | Check `spec.selector` on PVC and labels on PV |

```bash
# Debug binding
kubectl describe pvc my-pvc   # look at Events section
kubectl get pv                # check STATUS column
```
