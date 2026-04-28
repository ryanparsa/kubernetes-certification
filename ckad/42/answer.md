## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/service/

### Create the namespace

```bash
kubectl create namespace services
```

### Create the deployment and three services

```yaml
# lab/42.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: services
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: services
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-svc-cluster
  namespace: services
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: web-svc-nodeport
  namespace: services
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
  type: NodePort
---
apiVersion: v1
kind: Service
metadata:
  name: web-svc-lb
  namespace: services
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

```bash
kubectl apply -f lab/42.yaml
kubectl rollout status deployment/web-app -n services
```

### Verify

```bash
kubectl get services -n services
```

## Checklist (Score: 0/5)

- [ ] Namespace `services` exists
- [ ] Deployment `web-app` has 3 replicas with image `nginx:alpine` and label `app=web`
- [ ] ClusterIP service `web-svc-cluster` exposes port `80`
- [ ] NodePort service `web-svc-nodeport` exposes port `80` on nodePort `30080`
- [ ] LoadBalancer service `web-svc-lb` exposes port `80`
