# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 5. Jobs

A Job runs one or more pods to completion (exit code 0).

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
spec:
  completions: 1          # total pods that must succeed
  parallelism: 1          # pods running in parallel
  backoffLimit: 4         # retry limit before marking Job as failed
  activeDeadlineSeconds: 600
  template:
    spec:
      restartPolicy: Never   # Never or OnFailure (not Always)
      containers:
      - name: migrate
        image: my-migrator:latest
        command: ["python", "migrate.py"]
```

```bash
# Check Job status
kubectl get job db-migrate
kubectl describe job db-migrate

# Get logs from a completed Job pod
kubectl logs -l job-name=db-migrate
```

---
