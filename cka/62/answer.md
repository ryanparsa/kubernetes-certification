## Answer

**Reference:** https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

### Create the namespace

```bash
kubectl create namespace monitoring
```

### Create the Deployment and HPA

```yaml
# lab/62-hpa.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-consumer
  namespace: monitoring
spec:
  replicas: 3
  selector:
    matchLabels:
      app: resource-consumer
  template:
    metadata:
      labels:
        app: resource-consumer
    spec:
      containers:
      - name: resource-consumer
        image: gcr.io/kubernetes-e2e-test-images/resource-consumer:1.5
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: resource-consumer
  namespace: monitoring
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: resource-consumer
  minReplicas: 3
  maxReplicas: 6
  targetCPUUtilizationPercentage: 50
```

```bash
kubectl apply -f lab/62-hpa.yaml
kubectl wait deployment resource-consumer -n monitoring --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get deployment resource-consumer -n monitoring
kubectl get hpa resource-consumer -n monitoring
```

## Checklist (Score: 0/7)

- [ ] Deployment `resource-consumer` exists in `monitoring` namespace
- [ ] Deployment has `3` replicas using image `gcr.io/kubernetes-e2e-test-images/resource-consumer:1.5`
- [ ] CPU request is `100m` and memory request is `128Mi`
- [ ] CPU limit is `200m` and memory limit is `256Mi`
- [ ] HPA `resource-consumer` exists targeting the deployment
- [ ] HPA min replicas is `3`, max replicas is `6`
- [ ] HPA targets `50%` CPU utilization
