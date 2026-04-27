# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 6. CronJobs

Runs a Job on a schedule (cron syntax).

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
spec:
  schedule: "0 2 * * *"            # every day at 02:00
  timeZone: "UTC"
  concurrencyPolicy: Forbid        # Allow | Forbid | Replace
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 300     # how late a missed run can start
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: backup-tool:latest
            command: ["/backup.sh"]
```

| `concurrencyPolicy` | Effect |
|---|---|
| `Allow` | Multiple Job runs can overlap |
| `Forbid` | Skip new run if previous is still running |
| `Replace` | Cancel previous run and start new one |

---
