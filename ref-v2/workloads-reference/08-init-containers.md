# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 8. Init Containers

Run to completion **before** any app containers start. Used for setup tasks (wait for DB,
fetch secrets, populate volumes, etc.).

```yaml
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.35
    command: ['sh', '-c',
      'until nc -z mysql.my-db.svc.cluster.local 3306; do sleep 2; done']
  - name: db-migrate
    image: my-migrator:latest
    command: ["python", "migrate.py"]
  containers:
  - name: app
    image: my-app:v1
```

- Init containers run sequentially (in order)
- Each must exit 0 before the next starts
- If an init container fails, the pod restarts it (respecting `restartPolicy`)
- App containers don't start until all init containers succeed

---
