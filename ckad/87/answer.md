## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

### Create the namespace

```bash
kubectl create namespace jobs
```

### Create the CronJob

```bash
kubectl create cronjob backup-job \
  --image=busybox \
  --schedule="0 2 * * *" \
  --namespace=jobs \
  -- sh -c 'echo "Backup started at $(date)" && sleep 5 && echo "Backup complete"'
```

Then patch for the additional fields:

```bash
kubectl patch cronjob backup-job -n jobs --type=merge -p '{
  "spec": {
    "successfulJobsHistoryLimit": 3,
    "failedJobsHistoryLimit": 1,
    "concurrencyPolicy": "Forbid"
  }
}'
```

### Alternative — YAML approach

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

## Checklist (Score: 0/4)

- [ ] CronJob `backup-job` exists in namespace `jobs`
- [ ] Schedule is `0 2 * * *`
- [ ] `concurrencyPolicy` is `Forbid`
- [ ] `successfulJobsHistoryLimit: 3` and `failedJobsHistoryLimit: 1`
