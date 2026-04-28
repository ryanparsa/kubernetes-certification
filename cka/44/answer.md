## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

### Create the Deployment

```yaml
# lab/web-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: web-app
              topologyKey: kubernetes.io/hostname
      containers:
      - name: nginx
        image: nginx:1.19
```

```bash
kubectl apply -f lab/web-app.yaml
```

### Create the NodePort Service

```yaml
# lab/web-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: default
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: web-app
```

```bash
kubectl apply -f lab/web-service.yaml
```

### Verify

```bash
kubectl get deployment web-app
kubectl get svc web-service
kubectl get pods -l app=web-app -o wide
```

## Checklist (Score: 0/4)

- [ ] Deployment `web-app` exists with `3` replicas
- [ ] Deployment uses image `nginx:1.19`
- [ ] Service `web-service` of type `NodePort` exists and targets port `80`
- [ ] Pods have a pod anti-affinity rule for distribution across nodes
