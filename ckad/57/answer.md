## Answer

**Reference:** https://kubernetes.io/docs/reference/kubectl/cheatsheet/

### Create the namespace

```bash
kubectl create namespace pod-namespace
```

### Create the Pod with a named container

```bash
kubectl run pod-1 --image=nginx --dry-run=client -o yaml > lab/57.yaml
```

Edit `lab/57.yaml` and change the container name from `pod-1` to `container-1`:

```yaml
# lab/57.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pod-1
  name: pod-1
  namespace: pod-namespace
spec:
  containers:
  - image: nginx
    name: container-1
```

```bash
kubectl apply -f lab/57.yaml
kubectl wait pod/pod-1 -n pod-namespace --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod pod-1 -n pod-namespace -o jsonpath='{.spec.containers[0].name}'
```

## Checklist (Score: 0/2)

- [ ] Namespace `pod-namespace` exists
- [ ] Pod `pod-1` exists in `pod-namespace` with container named `container-1`
