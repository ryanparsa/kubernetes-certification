## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

### Create the deployment

```bash
kubectl create deployment webapp --image=nginx:1.20 --replicas=3 --port=80
kubectl get deployment webapp
```

### Update the image

```bash
kubectl set image deployment/webapp nginx=nginx:1.21
kubectl rollout status deployment/webapp
kubectl rollout history deployment/webapp
```

### Roll back to the previous revision

```bash
kubectl rollout undo deployment/webapp
kubectl rollout status deployment/webapp

# Verify the image reverted
kubectl get deployment webapp -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Expected: `nginx:1.20`

### Scale to 5 replicas

```bash
kubectl scale deployment webapp --replicas=5
kubectl get deployment webapp
```

### Configure rolling update strategy

```bash
kubectl patch deployment webapp -p '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'

# Verify
kubectl get deployment webapp -o jsonpath='{.spec.strategy.rollingUpdate}'
```

Alternatively, edit with a full manifest:

```yaml
# lab/webapp.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 5
  selector:
    matchLabels:
      app: webapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
        ports:
        - containerPort: 80
```

## Checklist (Score: 0/5)

- [ ] Deployment `webapp` created with `nginx:1.20` and 3 replicas
- [ ] Image updated to `nginx:1.21` via rolling update
- [ ] Rollback successful -- image is back to `nginx:1.20`
- [ ] Deployment scaled to 5 replicas
- [ ] Rolling update strategy set to `maxSurge: 1`, `maxUnavailable: 0`
