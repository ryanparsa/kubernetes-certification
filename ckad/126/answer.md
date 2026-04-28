## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment>

### Scale down Deployment to 0

```bash
kubectl scale deployment neptune-10ab -n neptune --replicas=0
kubectl get deployment neptune-10ab -n neptune
```

### Annotate Deployment for maintenance protection

```bash
kubectl annotate deployment neptune-20ab -n neptune admission.datree.io/warn="true"
kubectl get deployment neptune-20ab -n neptune -o yaml | grep -A5 annotations
```

### Verify

```bash
kubectl get deployments -n neptune
# neptune-10ab should show 0/0 READY
```

## Checklist (Score: 0/3)

- [ ] Deployment `neptune-10ab` scaled to 0 replicas
- [ ] Deployment `neptune-20ab` annotated with `admission.datree.io/warn: "true"`
- [ ] All Pods from `neptune-10ab` are terminated
