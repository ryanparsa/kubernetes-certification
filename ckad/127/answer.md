## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment>

### Perform the rolling update

```bash
kubectl set image deployment/api-new-c32 \
  <container-name>=httpd:2.4.41-alpine \
  -n neptune

kubectl rollout status deployment/api-new-c32 -n neptune
```

### Check rollout history

```bash
kubectl rollout history deployment/api-new-c32 -n neptune
```

### Roll back to previous version

```bash
kubectl rollout undo deployment/api-new-c32 -n neptune
kubectl rollout status deployment/api-new-c32 -n neptune
```

### Verify original image is restored

```bash
kubectl get pods -n neptune -o jsonpath='{.items[*].spec.containers[*].image}'
```

## Checklist (Score: 0/3)

- [ ] Rolling update to `httpd:2.4.41-alpine` completed successfully
- [ ] Deployment rolled back to the original image
- [ ] Pods are running with the original image after rollback
