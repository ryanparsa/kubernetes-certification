## Answer

**Reference:** https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

### Taint the node

```bash
kubectl taint node k3d-cluster-agent-1 special-workload=true:NoSchedule
```

### Create the namespace

```bash
kubectl create namespace scheduling
```

### Create the deployment that tolerates the taint

```yaml
# lab/54-toleration-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: toleration-deploy
  namespace: scheduling
spec:
  replicas: 2
  selector:
    matchLabels:
      app: toleration-deploy
  template:
    metadata:
      labels:
        app: toleration-deploy
    spec:
      tolerations:
      - key: "special-workload"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
      containers:
      - name: nginx
        image: nginx
```

### Create the deployment that avoids the tainted node

```yaml
# lab/54-normal-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: normal-deploy
  namespace: scheduling
spec:
  replicas: 2
  selector:
    matchLabels:
      app: normal-deploy
  template:
    metadata:
      labels:
        app: normal-deploy
    spec:
      containers:
      - name: nginx
        image: nginx
```

```bash
kubectl apply -f lab/54-toleration-deploy.yaml
kubectl apply -f lab/54-normal-deploy.yaml
kubectl wait deployment toleration-deploy -n scheduling --for=condition=Available --timeout=60s
kubectl wait deployment normal-deploy -n scheduling --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get pods -n scheduling -o wide
# toleration-deploy pods can run on k3d-cluster-agent-1
# normal-deploy pods run only on untainted nodes
```

## Checklist (Score: 0/6)

- [ ] Node `k3d-cluster-agent-1` has taint `special-workload=true:NoSchedule`
- [ ] Deployment `toleration-deploy` exists in `scheduling` namespace with `2` replicas
- [ ] `toleration-deploy` has a toleration for `special-workload=true:NoSchedule`
- [ ] Deployment `normal-deploy` exists in `scheduling` namespace with `2` replicas
- [ ] `normal-deploy` pods do not run on `k3d-cluster-agent-1`
- [ ] Both deployments are in `Running` state
