# Pod Lifecycle Events

```
Pending → (init containers) → Running → Succeeded / Failed
                                ↑
                           (CrashLoopBackOff if container keeps failing)
```

```bash
# Watch pod lifecycle
kubectl get pod my-pod -w

# Pod ready conditions
kubectl get pod my-pod -o jsonpath='{.status.conditions}'

# Container statuses
kubectl get pod my-pod -o jsonpath='{.status.containerStatuses[*].state}'
```

---

