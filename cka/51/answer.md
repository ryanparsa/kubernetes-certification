## Answer

**Reference:** https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

### Create the namespace

```bash
kubectl create namespace scaling
```

### Create the Deployment

```yaml
# lab/51-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scaling-app
  namespace: scaling
spec:
  replicas: 2
  selector:
    matchLabels:
      app: scaling-app
  template:
    metadata:
      labels:
        app: scaling-app
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

```bash
kubectl apply -f lab/51-deploy.yaml
kubectl wait deployment scaling-app -n scaling --for=condition=Available --timeout=60s
```

### Create the HorizontalPodAutoscaler

```yaml
# lab/51-hpa.yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: scaling-app
  namespace: scaling
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: scaling-app
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70
```

```bash
kubectl apply -f lab/51-hpa.yaml
```

### Verify

```bash
kubectl get deployment scaling-app -n scaling
kubectl get hpa scaling-app -n scaling
```

## Checklist (Score: 0/7)

- [ ] Deployment `scaling-app` exists in `scaling` namespace
- [ ] Deployment has `2` replicas
- [ ] Container image is `nginx`
- [ ] CPU request is `200m` and memory request is `256Mi`
- [ ] CPU limit is `500m` and memory limit is `512Mi`
- [ ] HPA `scaling-app` exists with min `2` / max `5` replicas
- [ ] HPA targets CPU utilization at `70%`
