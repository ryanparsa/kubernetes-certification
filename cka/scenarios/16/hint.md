# Hints — Task 16

## Solution

```bash
kubectl -n shop rollout history deployment/store
kubectl -n shop rollout undo deployment/store
kubectl -n shop rollout status deployment/store
```

To roll back to a specific revision number:
```bash
kubectl -n shop rollout undo deployment/store --to-revision=1
```
