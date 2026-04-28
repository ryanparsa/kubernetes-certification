## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>

### Create the Deployment

```bash
kubectl create deployment deploy --image=nginx --replicas=3 --dry-run=client -o yaml > lab/deploy.yaml
```

Edit `lab/deploy.yaml` to set the correct labels and container name:

```yaml
# lab/deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    tier: backend
  name: deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: v1
  template:
    metadata:
      labels:
        app: v1
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
```

```bash
kubectl apply -f lab/deploy.yaml
kubectl rollout status deployment/deploy
kubectl get deployments deploy
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# deploy   3/3     3            3           10s
```

### Update the image

```bash
kubectl set image deployment/deploy nginx=nginx:latest
kubectl rollout status deployment/deploy
```

### Scale to 5 replicas

```bash
kubectl scale deployment/deploy --replicas=5
kubectl get pods -l app=v1
```

### Inspect rollout history and rollback

```bash
kubectl rollout history deployment/deploy
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>

kubectl rollout undo deployment/deploy --to-revision=1
kubectl rollout status deployment/deploy
```

### Verify image after rollback

```bash
kubectl get pods -l app=v1 -o jsonpath='{.items[*].spec.containers[*].image}'
# nginx nginx nginx ...
```

## Checklist (Score: 0/6)

- [ ] Deployment `deploy` exists with label `tier=backend`
- [ ] Deployment has 3 replicas and pod label `app=v1`
- [ ] Container is named `nginx` and uses image `nginx`
- [ ] Rollout to `nginx:latest` completed successfully
- [ ] Deployment scaled to 5 replicas
- [ ] Deployment rolled back to revision 1 (image `nginx`)
