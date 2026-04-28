## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

### Create the namespace

```bash
kubectl create namespace jobs
```

### Create the CronJob

```yaml
# lab/backup-job.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
  namespace: jobs
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: busybox
            command:
            - sh
            - -c
            - 'echo "Backup started at $(date)" && sleep 5 && echo "Backup complete"'
          restartPolicy: OnFailure
```

```bash
kubectl apply -f lab/backup-job.yaml
```

### Verify

```bash
kubectl get cronjob backup-job -n jobs
kubectl describe cronjob backup-job -n jobs | grep -E "Schedule|Concurrency|Successful|Failed"
```

## Checklist (Score: 4/4)

- [x] CronJob `backup-job` exists in namespace `jobs`
- [x] Schedule is `0 2 * * *`
- [x] `concurrencyPolicy` is `Forbid`
- [x] `successfulJobsHistoryLimit: 3` and `failedJobsHistoryLimit: 1`
