# Horizontal Pod Autoscaler (HPA)

Scales a Deployment (or StatefulSet/ReplicaSet) based on metrics.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
  namespace: my-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50    # target 50% of CPU requests across all pods
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 200Mi
```

```bash
# Create HPA imperatively
kubectl autoscale deployment api-gateway \
  --cpu-percent=50 --min=2 --max=10 -n my-app

# Check HPA status
kubectl get hpa -n my-app
kubectl describe hpa api-gateway -n my-app

# HPA requires metrics-server to be installed
kubectl top pods -n my-app
```

> If the Deployment also has `spec.replicas` set, the HPA will immediately override it
> to `minReplicas`. Remove `replicas:` from the Deployment spec to avoid conflicts.

---

