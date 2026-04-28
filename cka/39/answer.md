## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/

### Create the static pod manifest

Place the manifest at `/etc/kubernetes/manifests/static-web.yaml` on the node:

```yaml
# /etc/kubernetes/manifests/static-web.yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-web
spec:
  containers:
  - name: nginx
    image: nginx:1.19
    ports:
    - containerPort: 80
```

### Verify

```bash
kubectl get pod -A | grep static-web
```

The kubelet will automatically pick up the manifest and create the pod.

## Checklist (Score: 0/5)

- [ ] Static pod manifest exists at `/etc/kubernetes/manifests/static-web.yaml`
- [ ] Manifest uses image `nginx:1.19`
- [ ] Container exposes port `80`
- [ ] Pod name is `static-web`
- [ ] Pod is Running
