## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/configmap/

### Create the namespace (if not present)

```bash
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -
```

### Create the ConfigMap

```bash
kubectl create configmap app-config -n workloads \
  --from-literal=APP_ENV=production \
  --from-literal=LOG_LEVEL=info
```

### Create the pod with ConfigMap environment variables

```yaml
# lab/config-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
  namespace: workloads
spec:
  containers:
  - name: nginx
    image: nginx
    env:
    - name: APP_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
```

```bash
kubectl apply -f lab/config-pod.yaml
```

### Verify

```bash
kubectl get pod config-pod -n workloads
kubectl exec config-pod -n workloads -- printenv APP_ENV LOG_LEVEL
```

## Checklist (Score: 0/4)

- [ ] ConfigMap `app-config` exists in namespace `workloads` with keys `APP_ENV=production` and `LOG_LEVEL=info`
- [ ] Pod `config-pod` is running in namespace `workloads`
- [ ] Pod has environment variables `APP_ENV` and `LOG_LEVEL` sourced from ConfigMap `app-config`
- [ ] Pod has correct resource requests and limits (cpu: 100m/200m, memory: 128Mi/256Mi)
