## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

### Create the pod manifest

```yaml
# lab/web.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  initContainers:
  - name: init
    image: busybox
    command: ["sh", "-c", "echo 'Hello from init' > /work-dir/index.html"]
    volumeMounts:
    - name: html
      mountPath: /work-dir
  containers:
  - name: nginx
    image: nginx:alpine
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
  volumes:
  - name: html
    emptyDir: {}
```

```bash
kubectl apply -f lab/web.yaml
kubectl get pod web
```

### Verify init container ran and nginx serves the content

Wait for the pod to reach `Running` state, then verify:

```bash
kubectl logs web -c init 2>/dev/null || echo "Init container already exited (expected)"
kubectl exec web -c nginx -- cat /usr/share/nginx/html/index.html
```

Expected output: `Hello from init`

You can also curl from within the cluster:

```bash
kubectl exec web -c nginx -- wget -qO- http://localhost/
```

## Checklist (Score: 0/4)

- [ ] Pod `web` is running
- [ ] Init container `init` ran and wrote `Hello from init` to the shared volume
- [ ] Volume `html` is shared between init and main containers
- [ ] nginx container serves the content written by the init container
