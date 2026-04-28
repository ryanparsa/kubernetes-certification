## Answer

**Reference:** https://kubernetes.io/docs/concepts/policy/resource-quotas/

### Create namespace and ResourceQuota

```bash
kubectl create namespace quota-ns
```

```yaml
# lab/ns-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ns-quota
  namespace: quota-ns
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 500Mi
    limits.cpu: "2"
    limits.memory: 1Gi
    pods: "4"
```

```bash
kubectl apply -f lab/ns-quota.yaml
kubectl describe resourcequota ns-quota -n quota-ns
```

### Create LimitRange

```yaml
# lab/container-limits.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: container-limits
  namespace: quota-ns
spec:
  limits:
  - type: Container
    default:
      cpu: 200m
      memory: 128Mi
    defaultRequest:
      cpu: 100m
      memory: 64Mi
```

```bash
kubectl apply -f lab/container-limits.yaml
kubectl describe limitrange container-limits -n quota-ns
```

### Create resource-pod with explicit requests and limits

```yaml
# lab/resource-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
  namespace: quota-ns
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: 250m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 256Mi
```

```bash
kubectl apply -f lab/resource-pod.yaml
kubectl get pod resource-pod -n quota-ns
kubectl describe resourcequota ns-quota -n quota-ns
```

The quota `Used` section should reflect the pod's resource consumption.

## Checklist (Score: 0/4)

- [ ] Namespace `quota-ns` exists
- [ ] ResourceQuota `ns-quota` created with correct CPU, memory, and pod limits
- [ ] LimitRange `container-limits` created with correct default requests and limits
- [ ] Pod `resource-pod` running in `quota-ns` with explicit requests and limits within quota
