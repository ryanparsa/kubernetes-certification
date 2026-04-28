## Answer

**Reference:** https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/

### Investigate the failing deployment

```bash
# Check the pods in the troubleshooting namespace
kubectl get pods -n troubleshooting

# Check the deployment status
kubectl describe deployment broken-app -n troubleshooting

# Check pod details for errors
kubectl describe pod -l app=broken-app -n troubleshooting

# Check logs of a failing pod
kubectl logs <pod-name> -n troubleshooting
```

### Fix the deployment

Depending on the root cause, apply the appropriate fix:

If the container image is incorrect:

```bash
kubectl set image deployment/broken-app -n troubleshooting app=nginx:latest
```

If resource limits are too restrictive:

```bash
kubectl patch deployment broken-app -n troubleshooting \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","resources":{"limits":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

### Verify

```bash
kubectl rollout status deployment/broken-app -n troubleshooting
kubectl get pods -n troubleshooting -l app=broken-app
```

## Checklist (Score: 0/2)

- [ ] Deployment `broken-app` pods are running in namespace `troubleshooting`
- [ ] Deployment uses a valid container image
