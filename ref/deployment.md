# Deployments

Manages a ReplicaSet and provides rolling updates and rollbacks.

### Deployment strategies

| Strategy | Effect |
|---|---|
| `RollingUpdate` (default) | Gradually replaces old pods; zero downtime if configured correctly |
| `Recreate` | Terminates ALL old pods before creating new ones; causes downtime |

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1     # max pods that can be unavailable during rollout
      maxSurge: 1           # max extra pods created above desired replica count
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: app
        image: my-image:v2
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
```

```yaml
strategy:
  type: Recreate            # simpler; all old pods killed before new ones start
```

### Rollout commands

```bash
# Check rollout status
kubectl rollout status deployment/api-gateway -n my-app

# View rollout history
kubectl rollout history deployment/api-gateway -n my-app

# Rollback to previous version
kubectl rollout undo deployment/api-gateway -n my-app

# Rollback to a specific revision
kubectl rollout undo deployment/api-gateway --to-revision=2 -n my-app

# Pause a rollout
kubectl rollout pause deployment/api-gateway -n my-app

# Resume a rollout
kubectl rollout resume deployment/api-gateway -n my-app

# Scale
kubectl scale deployment api-gateway --replicas=5 -n my-app
```

---

