## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

### Create the namespace

```bash
kubectl create namespace backend
```

### Create the multi-container Pod with init container

```yaml
# lab/app-stack.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-stack
  namespace: backend
spec:
  initContainers:
  - name: init-db
    image: busybox
    command: ["sh", "-c", "sleep 2"]
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
  containers:
  - name: app
    image: nginx:1.25
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
  - name: cache
    image: redis:7
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
```

```bash
kubectl apply -f lab/app-stack.yaml
kubectl wait pod/app-stack -n backend --for=condition=Ready --timeout=120s
```

### Verify

```bash
kubectl get pod app-stack -n backend
kubectl describe pod app-stack -n backend | grep -A 2 "Init Containers\|Containers"
```

## Checklist (Score: 0/3)

- [ ] Namespace `backend` exists
- [ ] Pod `app-stack` in namespace `backend` is Running with init container `init-db` and main containers `app` and `cache`
- [ ] All containers have CPU request `50m` and memory request `64Mi`
