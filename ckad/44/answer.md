## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

### Create the namespace

```bash
kubectl create namespace pod-design
```

### Create the CronJob

```yaml
# lab/44.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pod-design
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
  namespace: pod-design
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      activeDeadlineSeconds: 100
      template:
        spec:
          containers:
          - name: backup
            image: busybox
            command: ['sh', '-c', 'echo Backup started: $(date); sleep 30; echo Backup completed: $(date)']
          restartPolicy: OnFailure
```

```bash
kubectl apply -f lab/44.yaml
```

### Verify

```bash
kubectl get cronjob backup-job -n pod-design
kubectl describe cronjob backup-job -n pod-design | grep -E "Schedule|Deadline|Restart"
```

## Checklist (Score: 0/4)

- [ ] Namespace `pod-design` exists
- [ ] CronJob `backup-job` has schedule `*/5 * * * *`
- [ ] CronJob uses image `busybox` with correct command
- [ ] CronJob has restart policy `OnFailure` and active deadline of `100` seconds
