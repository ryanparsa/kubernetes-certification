# State and Lifecycle

**Kustomize does not track state.** It does not know which resources it previously created.

- Adding a resource to kustomize YAML and applying → resource is created
- Removing a resource from kustomize YAML and applying → resource is **NOT deleted**
  (you must delete it manually with `kubectl delete`)

This is different from Helm, which tracks state in a release and deletes removed resources.

```bash
# Kustomize won't delete this — must be done manually
kubectl delete configmap horizontal-scaling-config -n api-gateway-staging
kubectl delete configmap horizontal-scaling-config -n api-gateway-prod
```

---

