## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment

### Create the namespace

```bash
kubectl create namespace upgrade
mkdir -p /tmp/exam
```

### Create the initial Deployment

```yaml
# lab/65-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v1
  namespace: upgrade
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: app-v1
  template:
    metadata:
      labels:
        app: app-v1
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
```

```bash
kubectl apply -f lab/65-deploy.yaml
kubectl wait deployment app-v1 -n upgrade --for=condition=Available --timeout=60s
```

### Perform the rolling update

```bash
kubectl set image deployment/app-v1 nginx=nginx:1.20 -n upgrade
kubectl rollout status deployment/app-v1 -n upgrade
```

### Save rollout history

```bash
kubectl rollout history deployment app-v1 -n upgrade > /tmp/exam/rollout-history.txt
cat /tmp/exam/rollout-history.txt
```

### Roll back to the previous version

```bash
kubectl rollout undo deployment/app-v1 -n upgrade
kubectl rollout status deployment/app-v1 -n upgrade
```

### Verify

```bash
kubectl get deployment app-v1 -n upgrade
kubectl get pods -n upgrade -o jsonpath='{.items[*].spec.containers[0].image}'
# Should show nginx:1.19 after rollback
```

## Checklist (Score: 0/7)

- [ ] Deployment `app-v1` exists in `upgrade` namespace with `4` replicas
- [ ] Initial image is `nginx:1.19`
- [ ] RollingUpdate strategy with `maxUnavailable: 1` and `maxSurge: 1`
- [ ] Rolling update to `nginx:1.20` was performed
- [ ] Rollout history saved to `/tmp/exam/rollout-history.txt`
- [ ] Deployment rolled back to previous version (`nginx:1.19`)
- [ ] All 4 pods are `Running` after rollback
