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

### Add delete protection (Finalizer)

A common way to prevent accidental deletion is to add a finalizer.

```bash
kubectl patch deployment neptune-20ab -n neptune -p '{"metadata":{"finalizers":["kubernetes.io/prevent-deletion"]}}' --type=merge
```

Also, adding the requested annotation (though it doesn't provide technical protection):

```bash
kubectl annotate deployment neptune-20ab -n neptune kubectl.kubernetes.io/last-applied-configuration='{"apiVersion":"apps/v1","kind":"Deployment","metadata":{"name":"neptune-20ab","namespace":"neptune"}}'
```

### Verify

```bash
kubectl get deployments -n neptune
# neptune-10ab should show 0/0 READY
```

## Checklist (Score: 0/4)

- [ ] Deployment `neptune-10ab` scaled to 0 replicas
- [ ] All Pods from `neptune-10ab` are terminated
- [ ] Deployment `neptune-20ab` annotated with `admission.datree.io/warn: "true"`
- [ ] Deployment `neptune-20ab` protected from accidental deletion
