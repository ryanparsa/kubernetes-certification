## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/pods/init-containers/>

### Investigate the existing Deployment

```bash
kubectl get deployment war-department -n war -o yaml
kubectl get configmap war-department-config -n war -o yaml
```

### Create the Pod with ConfigMap volume mount

```yaml
# lab/war-department-check.yaml
apiVersion: v1
kind: Pod
metadata:
  name: war-department-check
  namespace: default
spec:
  containers:
  - name: war-department-check
    image: busybox:1.31.0
    command: ["sleep", "9999"]
    volumeMounts:
    - name: war-config
      mountPath: /tmp/war-config
  volumes:
  - name: war-config
    configMap:
      name: war-department-config
```

```bash
kubectl apply -f lab/war-department-check.yaml
kubectl logs war-department-check > /opt/course/17/pod_logs.log
cat /opt/course/17/pod_logs.log
```

## Checklist (Score: 0/3)

- [ ] Pod `war-department-check` running with image `busybox:1.31.0` and command `sleep 9999`
- [ ] ConfigMap `war-department-config` mounted as volume at `/tmp/war-config`
- [ ] Pod logs written to `/opt/course/17/pod_logs.log`
