## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

### Create the namespace

```bash
kubectl create namespace monitoring
```

### Create the pod with resource constraints

```yaml
# lab/resource-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
  namespace: monitoring
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "200m"
        memory: "256Mi"
```

```bash
kubectl apply -f lab/resource-pod.yaml
```

### Verify

```bash
kubectl get pod resource-pod -n monitoring
kubectl describe pod resource-pod -n monitoring | grep -A8 Limits
```

## Checklist (Score: 0/5)

- [ ] Pod `resource-pod` exists in namespace `monitoring`
- [ ] CPU request is `100m`
- [ ] CPU limit is `200m`
- [ ] Memory request is `128Mi`
- [ ] Memory limit is `256Mi`
