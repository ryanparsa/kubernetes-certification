## Answer

**Reference:** https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/

### Create the namespace

```bash
kubectl create namespace quota-namespace
```

### Create the ResourceQuota

```bash
kubectl create quota my-quota -n quota-namespace --hard=cpu=500m,memory=2Gi
```

### Create the LimitRange

```yaml
# lab/59-limitrange.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: my-limit
  namespace: quota-namespace
spec:
  limits:
  - max:
      memory: 1Gi
      cpu: 250m
    type: Pod
```

```bash
kubectl apply -f lab/59-limitrange.yaml
```

### Verify

```bash
kubectl get quota my-quota -n quota-namespace
kubectl get limitrange my-limit -n quota-namespace
kubectl describe limitrange my-limit -n quota-namespace
```

## Checklist (Score: 0/3)

- [ ] Namespace `quota-namespace` exists
- [ ] ResourceQuota `my-quota` has hard limits `cpu=500m` and `memory=2Gi`
- [ ] LimitRange `my-limit` restricts Pods to max `1Gi` memory and `250m` CPU
