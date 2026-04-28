## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/

### Create the namespace

```bash
kubectl create namespace mynamespace
```

### Create the nginx pod imperatively

```bash
kubectl run nginx --image=nginx --namespace=mynamespace
kubectl get pod nginx -n mynamespace
```

### Exec into the nginx pod

```bash
kubectl exec -it nginx -n mynamespace -- printenv HOSTNAME
```

### Create envpod from YAML

```yaml
# lab/envpod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: envpod
  namespace: mynamespace
spec:
  restartPolicy: Never
  containers:
  - name: busybox
    image: busybox
    command: ["env"]
```

```bash
kubectl apply -f lab/envpod.yaml
```

### Retrieve envpod logs

```bash
kubectl logs envpod -n mynamespace
```

The output should list all environment variables available inside the container.

## Checklist (Score: 0/5)

- [ ] Namespace `mynamespace` exists
- [ ] Pod `nginx` is running in namespace `mynamespace`
- [ ] Exec into `nginx` pod prints `HOSTNAME` value
- [ ] Pod `envpod` created from YAML manifest with `restartPolicy: Never`
- [ ] `kubectl logs envpod` shows environment variable output
