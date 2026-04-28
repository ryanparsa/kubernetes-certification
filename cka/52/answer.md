## Answer

**Reference:** https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity

### Label the target node

```bash
kubectl label node k3d-cluster-agent-1 disk=ssd
```

### Create the namespace

```bash
kubectl create namespace scheduling
```

### Create the Deployment with node affinity

```yaml
# lab/52-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-scheduling
  namespace: scheduling
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app-scheduling
  template:
    metadata:
      labels:
        app: app-scheduling
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: disk
                operator: In
                values:
                - ssd
      containers:
      - name: nginx
        image: nginx
```

```bash
kubectl apply -f lab/52-deploy.yaml
kubectl wait deployment app-scheduling -n scheduling --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get pods -n scheduling -o wide
# All pods should be on k3d-cluster-agent-1
```

## Checklist (Score: 0/5)

- [ ] Node `k3d-cluster-agent-1` has label `disk=ssd`
- [ ] Deployment `app-scheduling` exists in `scheduling` namespace
- [ ] Deployment has `3` replicas using `nginx` image
- [ ] Deployment uses `requiredDuringSchedulingIgnoredDuringExecution` node affinity (not nodeSelector)
- [ ] All pods are scheduled on `k3d-cluster-agent-1`
