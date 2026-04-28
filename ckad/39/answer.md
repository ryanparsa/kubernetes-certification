## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

### Create the namespace

```bash
kubectl create namespace pod-design
```

### Create the deployment and service

```yaml
# lab/39.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pod-design
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: pod-design
  labels:
    app: frontend
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      tier: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:1.19.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-svc
  namespace: pod-design
spec:
  selector:
    app: frontend
    tier: frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

```bash
kubectl apply -f lab/39.yaml
kubectl rollout status deployment/frontend -n pod-design
```

### Verify

```bash
kubectl get deployment frontend -n pod-design
kubectl get service frontend-svc -n pod-design
```

## Checklist (Score: 0/4)

- [ ] Namespace `pod-design` exists
- [ ] Deployment `frontend` is created with 3 replicas and image `nginx:1.19.0`
- [ ] Deployment has labels `app=frontend` and `tier=frontend`
- [ ] Service `frontend-svc` of type `ClusterIP` exposes port `80`
