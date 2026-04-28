## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory

### Create the namespace

```bash
kubectl create namespace deployment-namespace
```

### Create the Deployment

```bash
kubectl create deployment my-deployment --image=nginx --replicas=3 --port=80 \
  --namespace=deployment-namespace --dry-run=client -o yaml > lab/60.yaml
```

Edit `lab/60.yaml` to set the container name and resource requests/limits:

```yaml
# lab/60.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  namespace: deployment-namespace
  labels:
    app: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-deployment
  template:
    metadata:
      labels:
        app: my-deployment
    spec:
      containers:
      - image: nginx
        name: my-container
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "25Mi"
          limits:
            memory: "100Mi"
```

```bash
kubectl apply -f lab/60.yaml
kubectl wait deployment/my-deployment -n deployment-namespace --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get deployment my-deployment -n deployment-namespace
kubectl get pods -n deployment-namespace
kubectl describe deployment my-deployment -n deployment-namespace | grep -E 'Image|Memory|Container'
```

## Checklist (Score: 0/4)

- [ ] Namespace `deployment-namespace` exists
- [ ] Deployment `my-deployment` has `3` replicas running in `deployment-namespace`
- [ ] Container is named `my-container` and exposes port `80`
- [ ] Container has memory request `25Mi` and memory limit `100Mi`
