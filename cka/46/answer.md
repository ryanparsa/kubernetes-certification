## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/configmap/

### Create the ConfigMap

```bash
kubectl create configmap app-config --from-literal=APP_COLOR=blue
```

### Create the pod mounting the ConfigMap as a volume

```yaml
# lab/config-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

```bash
kubectl apply -f lab/config-pod.yaml
```

### Verify

```bash
kubectl get configmap app-config -o yaml
kubectl exec config-pod -- cat /etc/config/APP_COLOR
```

## Checklist (Score: 0/7)

- [ ] ConfigMap `app-config` exists in namespace `default`
- [ ] ConfigMap has key `APP_COLOR` with value `blue`
- [ ] Pod `config-pod` exists in namespace `default`
- [ ] Pod uses image `nginx`
- [ ] Volume named `config-volume` is defined and backed by ConfigMap `app-config`
- [ ] Volume is mounted at `/etc/config` in the container
- [ ] File `/etc/config/APP_COLOR` is accessible inside the pod
