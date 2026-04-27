# Kubernetes Troubleshooting Reference — 2. Pod Crash-Loop Debugging

> Part of [Kubernetes Troubleshooting Reference](../Troubleshooting Reference.md)


### Symptoms
- `CrashLoopBackOff`, `Error`, `OOMKilled`, `RunContainerError`

### Diagnosis steps

```bash
# 1. Get pod status and events
kubectl describe pod <pod> -n <ns>
# Look at: State, Last State, Exit Code, Restart Count, Events

# 2. Get current logs
kubectl logs <pod> -n <ns>

# 3. Get logs from the previous (crashed) container
kubectl logs <pod> -n <ns> --previous

# 4. For multi-container pods, specify container
kubectl logs <pod> -n <ns> -c <container>

# 5. Exec into a running container for live debugging
kubectl exec -it <pod> -n <ns> -- sh

# 6. If the image has no shell, use an ephemeral debug container
kubectl debug -it <pod> -n <ns> \
  --image=busybox:1.35 \
  --target=<main-container>

# 7. Check resource pressure (OOMKilled)
kubectl describe node <node> | grep -A 5 "Conditions:"
kubectl top pod <pod> -n <ns>
```

### Exit code reference

| Exit code | Meaning |
|---|---|
| 0 | Exited cleanly (expected) |
| 1 | Application error |
| 137 | OOMKilled (exit 128 + signal 9) |
| 139 | Segmentation fault (signal 11) |
| 143 | Graceful termination (SIGTERM, signal 15) |
| 255 | Entry point not found or exec error |

---

