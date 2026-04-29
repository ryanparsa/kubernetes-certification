## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

### CronJob 1 -- logger

```yaml
# lab/logger.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: logger
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: logger
            image: busybox
            command: ["sh", "-c", "date; echo Hello from the cluster"]
```

```bash
kubectl apply -f lab/logger.yaml
kubectl get cronjob logger
```

### Manually trigger a job from the CronJob

```bash
kubectl create job logger-manual --from=cronjob/logger
kubectl get jobs
kubectl logs job/logger-manual
```

### CronJob 2 -- limited (startingDeadlineSeconds)

```yaml
# lab/limited.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: limited
spec:
  schedule: "*/1 * * * *"
  startingDeadlineSeconds: 17
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: limited
            image: busybox
            command: ["date"]
```

```bash
kubectl apply -f lab/limited.yaml
kubectl get cronjob limited -o jsonpath='{.spec.startingDeadlineSeconds}'
```

Expected: `17`

## Checklist (Score: 0/3)

- [ ] CronJob `logger` created with schedule `*/1 * * * *` running `date; echo Hello from the cluster`
- [ ] Manual job created from `logger` CronJob using `kubectl create job --from`
- [ ] CronJob `limited` has `startingDeadlineSeconds: 17`
