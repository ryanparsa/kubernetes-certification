# Hints — Task 12

## Hint 1
Kustomize supports inline strategic-merge patches via the `patches` field with a `target`.

## Solution

Edit `k8s/overlays/prod/kustomization.yaml`:

```yaml
namespace: ops
resources:
- ../../base
patches:
- target:
    kind: Deployment
    name: api
  patch: |
    - op: replace
      path: /spec/replicas
      value: 4
```

Apply:
```bash
kubectl apply -k k8s/overlays/prod
kubectl -n ops rollout status deployment/api
```
