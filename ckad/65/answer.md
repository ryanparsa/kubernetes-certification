## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment

### Check rollout status

```bash
kubectl rollout status deployment/my-revision-deployment -n revision-namespace
```

### View revision history

```bash
kubectl rollout history deployment/my-revision-deployment -n revision-namespace
```

Expected output shows multiple revisions, with the latest one using a broken image:

```console
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
4         <none>   ← broken (e.g. image: ngin:1.21.0)
```

### Undo to the previous revision

```bash
kubectl rollout undo deployment/my-revision-deployment -n revision-namespace
kubectl rollout status deployment/my-revision-deployment -n revision-namespace
```

### Roll back to a specific earlier revision

```bash
kubectl rollout undo deployment/my-revision-deployment --to-revision=2 -n revision-namespace
kubectl rollout status deployment/my-revision-deployment -n revision-namespace
```

### Verify

```bash
kubectl describe deployment my-revision-deployment -n revision-namespace | grep Image
kubectl rollout history deployment/my-revision-deployment -n revision-namespace
```

## Checklist (Score: 0/3)

- [ ] Rollout history of `my-revision-deployment` inspected
- [ ] Deployment successfully rolled back to the previous revision
- [ ] Deployment successfully rolled back to revision `2`
