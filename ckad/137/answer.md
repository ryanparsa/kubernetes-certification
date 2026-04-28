## Answer

**Reference:** <https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/>

### Investigate the issue

```bash
kubectl get deployment mars-1274 -n mars
kubectl get pods -n mars
kubectl describe pod <pod-name> -n mars
kubectl logs <pod-name> -n mars
# Look for CrashLoopBackOff, wrong image, bad command, missing resource, etc.
```

### Fix the Deployment

```bash
# Example: fix a wrong image
kubectl set image deployment/mars-1274 <container>=<correct-image> -n mars

# Or edit directly
kubectl edit deployment mars-1274 -n mars

kubectl rollout status deployment/mars-1274 -n mars
```

### Test the fix

```bash
kubectl run test --image=busybox:1.31.0 -it --rm --restart=Never -n mars -- \
  wget -O- mars-svc
```

### Document the problem

```bash
echo "The Deployment mars-1274 had <describe problem here>." > /opt/course/18/reason.txt
```

## Checklist (Score: 0/3)

- [ ] Deployment `mars-1274` fixed and Pods running without `CrashLoopBackOff`
- [ ] Service `mars-svc` responds to requests from within the cluster
- [ ] Problem description written to `/opt/course/18/reason.txt`
