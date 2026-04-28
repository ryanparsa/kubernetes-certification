## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/configmap/>

### Create the ConfigMap

```bash
kubectl create configmap trauerweide --from-literal=tree=trauerweide
```

### Create the Pod with emptyDir volume

```yaml
# lab/pod-6.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-6
  namespace: default
spec:
  containers:
  - name: pod-6
    image: busybox:1.31.0
    command: ["sleep", "999"]
    volumeMounts:
    - name: data
      mountPath: /tmp/vols
  volumes:
  - name: data
    emptyDir: {}
```

```bash
kubectl apply -f lab/pod-6.yaml
kubectl get pod pod-6
kubectl get configmap trauerweide -o yaml
```

## Checklist (Score: 0/3)

- [ ] ConfigMap `trauerweide` exists with `tree=trauerweide`
- [ ] Pod `pod-6` running with image `busybox:1.31.0` and command `sleep 999`
- [ ] Pod has `emptyDir` volume mounted at `/tmp/vols`
