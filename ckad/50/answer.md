## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

### Create the namespace and service

```yaml
# lab/50.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: init-containers
---
apiVersion: v1
kind: Service
metadata:
  name: myservice
  namespace: init-containers
spec:
  selector:
    app: myservice
  ports:
  - port: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: app-with-init
  namespace: init-containers
spec:
  initContainers:
  - name: sidecar-container
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done']
    volumeMounts:
    - name: log-volume
      mountPath: /shared
  containers:
  - name: main-container
    image: nginx
    volumeMounts:
    - name: log-volume
      mountPath: /shared
  volumes:
  - name: log-volume
    emptyDir: {}
```

```bash
kubectl apply -f lab/50.yaml
kubectl wait pod/app-with-init -n init-containers --for=condition=Ready --timeout=120s
```

### Verify

```bash
kubectl get pod app-with-init -n init-containers
kubectl describe pod app-with-init -n init-containers | grep -A5 "Init Containers\|Containers:"
```

## Checklist (Score: 0/4)

- [ ] Namespace `init-containers` exists
- [ ] Pod `app-with-init` is created with init container and main container
- [ ] Service `myservice` is created correctly
- [ ] Shared volume `log-volume` is mounted at `/shared` in both init and main containers
