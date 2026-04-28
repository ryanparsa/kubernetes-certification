## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

### Identify the high-CPU container

```bash
kubectl get pod logging-pod -n troubleshooting -o yaml
kubectl top pod logging-pod -n troubleshooting --containers
```

### Add resource limits to the pod

Because pods are immutable regarding resource limits, replace the pod:

```bash
kubectl get pod logging-pod -n troubleshooting -o yaml > /tmp/logging-pod.yaml
```

Edit `/tmp/logging-pod.yaml` and add resource limits to the offending container:

```yaml
    resources:
      limits:
        cpu: 100m
        memory: 50Mi
```

```bash
kubectl replace -f /tmp/logging-pod.yaml --force
```

### Verify

```bash
kubectl get pod logging-pod -n troubleshooting
kubectl describe pod logging-pod -n troubleshooting | grep -A4 Limits
```

## Checklist (Score: 0/2)

- [ ] Container in `logging-pod` has CPU limit set to `100m`
- [ ] Container in `logging-pod` has memory limit set to `50Mi` and pod is running
