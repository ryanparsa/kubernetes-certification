## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/

### Create the namespace

```bash
kubectl create namespace core-concepts
```

### Create the pod with labels

```bash
kubectl run nginx-pod --image=nginx -n core-concepts --labels="app=web,env=prod"
```

Or using a YAML manifest:

```yaml
# lab/37.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: core-concepts
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  namespace: core-concepts
  labels:
    app: web
    env: prod
spec:
  containers:
  - name: nginx
    image: nginx
```

```bash
kubectl apply -f lab/37.yaml
```

### Verify

```bash
kubectl get pod nginx-pod -n core-concepts --show-labels
kubectl get pod nginx-pod -n core-concepts -o jsonpath='{.metadata.labels}'
```

## Checklist (Score: 0/4)

- [ ] Namespace `core-concepts` exists
- [ ] Pod `nginx-pod` is created in namespace `core-concepts`
- [ ] Pod uses image `nginx`
- [ ] Pod has labels `app=web` and `env=prod`
