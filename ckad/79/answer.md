## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

### Create the namespace

```bash
kubectl create namespace workloads
```

### Create the Pod with labels and resource constraints

```bash
kubectl run web --image=nginx:1.25 -n workloads \
  --labels="app=web,tier=frontend" \
  --dry-run=client -o yaml > lab/web-pod.yaml
```

Edit `lab/web-pod.yaml` to add the `resources` block, then apply:

```yaml
# lab/web-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web
  namespace: workloads
  labels:
    app: web
    tier: frontend
spec:
  containers:
  - name: web
    image: nginx:1.25
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 250m
        memory: 256Mi
```

```bash
kubectl apply -f lab/web-pod.yaml
kubectl wait pod/web -n workloads --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod web -n workloads --show-labels
kubectl describe pod web -n workloads | grep -A 4 "Limits\|Requests"
```

## Checklist (Score: 0/3)

- [ ] Namespace `workloads` exists
- [ ] Pod `web` in namespace `workloads` is Running with labels `app=web` and `tier=frontend`
- [ ] Container has CPU request `100m`/limit `250m` and memory request `128Mi`/limit `256Mi`
