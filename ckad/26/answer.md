## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

### Create the namespace (if not present)

```bash
kubectl create namespace workloads --dry-run=client -o yaml | kubectl apply -f -
```

### Create the CronJob

```yaml
# lab/log-cleaner.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: log-cleaner
  namespace: workloads
spec:
  schedule: "0 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: log-cleaner
            image: busybox
            command: ["/bin/sh", "-c"]
            args:
            - find /var/log -type f -name "*.log" -mtime +7 -delete
          restartPolicy: OnFailure
```

```bash
kubectl apply -f lab/log-cleaner.yaml
```

### Verify

```bash
kubectl get cronjob log-cleaner -n workloads
kubectl describe cronjob log-cleaner -n workloads
```

## Checklist (Score: 0/4)

- [ ] CronJob `log-cleaner` exists in namespace `workloads`
- [ ] CronJob schedule is `0 * * * *` (every hour)
- [ ] CronJob runs command `find /var/log -type f -name "*.log" -mtime +7 -delete`
- [ ] CronJob has `concurrencyPolicy: Forbid`, `successfulJobsHistoryLimit: 3`, and `failedJobsHistoryLimit: 1`
