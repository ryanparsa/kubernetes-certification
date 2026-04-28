## Answer

**Reference:** https://gateway-api.sigs.k8s.io/guides/

### Create the namespace

```bash
kubectl create namespace gateway
```

### Create Gateway, HTTPRoute, Deployments, and Services

```yaml
# lab/60-gateway.yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: main-gateway
  namespace: gateway
spec:
  gatewayClassName: standard
  listeners:
  - name: http
    port: 80
    protocol: HTTP
---
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: app-routes
  namespace: gateway
spec:
  parentRefs:
  - name: main-gateway
  rules:
  - matches:
    - path:
        value: /app1
    backendRefs:
    - name: app1-svc
      port: 8080
  - matches:
    - path:
        value: /app2
    backendRefs:
    - name: app2-svc
      port: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1
  namespace: gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: v1
kind: Service
metadata:
  name: app1-svc
  namespace: gateway
spec:
  selector:
    app: app1
  ports:
  - port: 8080
    targetPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2
  namespace: gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app2
  template:
    metadata:
      labels:
        app: app2
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: v1
kind: Service
metadata:
  name: app2-svc
  namespace: gateway
spec:
  selector:
    app: app2
  ports:
  - port: 8080
    targetPort: 80
```

```bash
kubectl apply -f lab/60-gateway.yaml
kubectl wait deployment app1 app2 -n gateway --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get gateway main-gateway -n gateway
kubectl get httproute app-routes -n gateway
kubectl get svc -n gateway
```

## Checklist (Score: 0/6)

- [ ] Gateway `main-gateway` exists in `gateway` namespace listening on port `80`
- [ ] HTTPRoute `app-routes` routes `/app1` to `app1-svc:8080`
- [ ] HTTPRoute routes `/app2` to `app2-svc:8080`
- [ ] Deployment `app1` and service `app1-svc` exist in `gateway` namespace
- [ ] Deployment `app2` and service `app2-svc` exist in `gateway` namespace
- [ ] Both deployments are `Running`
