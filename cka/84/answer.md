## Answer

**Reference:** https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

### 1. Remove ConfigMap and scale Deployment to 0

```bash
# In api-gateway-staging
kubectl delete configmap api-gateway-autoscaler -n api-gateway-staging
kubectl scale deployment api-gateway --replicas=0 -n api-gateway-staging

# In api-gateway-prod
kubectl delete configmap api-gateway-autoscaler -n api-gateway-prod
kubectl scale deployment api-gateway --replicas=0 -n api-gateway-prod
```

### 2. Create HorizontalPodAutoscaler

```bash
# In api-gateway-staging
kubectl autoscale deployment api-gateway --name=gateway --min=2 --max=3 --cpu-percent=50 -n api-gateway-staging

# In api-gateway-prod
kubectl autoscale deployment api-gateway --name=gateway --min=2 --max=3 --cpu-percent=50 -n api-gateway-prod
```

Alternatively, you can use YAML:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gateway
  namespace: api-gateway-staging
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 2
  maxReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

## Checklist (Score: 4/4)

- [ ] ConfigMap `api-gateway-autoscaler` removed in both namespaces
- [ ] Deployment `api-gateway` replicas set to `0` in both namespaces
- [ ] HPA `gateway` created in `api-gateway-staging` (min 2, max 3, 50% CPU)
- [ ] HPA `gateway` created in `api-gateway-prod` (min 2, max 3, 50% CPU)
