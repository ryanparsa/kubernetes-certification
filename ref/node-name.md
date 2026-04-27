# nodeName (Direct Assignment)

Bypasses the scheduler entirely. Pod is placed on the named node unconditionally.

```yaml
spec:
  nodeName: worker-1
  containers:
  - name: app
    image: nginx
```

> Use for manual scheduling (e.g. when kube-scheduler is stopped) or for debugging.
> Not recommended in production — the scheduler's resource checks are bypassed.

---

