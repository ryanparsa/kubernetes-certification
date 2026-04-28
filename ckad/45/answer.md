## Answer

**Reference:** https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/

### Investigate the broken deployment

```bash
kubectl get deployment broken-deployment -n troubleshooting
kubectl describe deployment broken-deployment -n troubleshooting
kubectl get pods -n troubleshooting
kubectl describe pod -l app=broken-deployment -n troubleshooting
```

### Common fixes

**Fix 1 — Correct the image:**

```bash
kubectl set image deployment/broken-deployment nginx=nginx:1.19 -n troubleshooting
```

**Fix 2 — Relax resource constraints (if requests are too high):**

```bash
kubectl patch deployment broken-deployment -n troubleshooting \
  --patch '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"cpu":"100m","memory":"128Mi"},"limits":{"cpu":"200m","memory":"256Mi"}}}]}}}}'
```

**Fix 3 — Remove a blocking NetworkPolicy (if present):**

```bash
kubectl get networkpolicies -n troubleshooting
kubectl delete networkpolicy <policy-name> -n troubleshooting
```

**Fix 4 — Edit the deployment directly:**

```bash
kubectl edit deployment broken-deployment -n troubleshooting
```

### Verify

```bash
kubectl rollout status deployment/broken-deployment -n troubleshooting
kubectl get pods -n troubleshooting
```

## Checklist (Score: 0/3)

- [ ] Deployment `broken-deployment` has 3 replicas
- [ ] All 3 pods are in `Running` state
- [ ] Pods are using the correct image `nginx:1.19`
