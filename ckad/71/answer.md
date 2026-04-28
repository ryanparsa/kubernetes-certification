## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/controllers/job/> | <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>

### Job with completions and parallelism

```bash
kubectl create job busybox-job --image=busybox --dry-run=client -o yaml \
  -- /bin/sh -c 'echo hello; sleep 5; echo world' > lab/busybox-job.yaml
```

Edit `lab/busybox-job.yaml` to add `completions: 5` and `parallelism: 2`:

```yaml
# lab/busybox-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: busybox-job
spec:
  completions: 5
  parallelism: 2
  template:
    spec:
      containers:
      - name: busybox-job
        image: busybox
        command:
        - /bin/sh
        - -c
        - echo hello; sleep 5; echo world
      restartPolicy: Never
```

```bash
kubectl apply -f lab/busybox-job.yaml
kubectl get jobs -w
# NAME          COMPLETIONS   DURATION   AGE
# busybox-job   5/5           35s        40s
```

### CronJob with startingDeadlineSeconds

```bash
kubectl create cronjob hello-cron \
  --image=busybox \
  --schedule="*/1 * * * *" \
  --dry-run=client -o yaml \
  -- /bin/sh -c 'date; echo Hello from Kubernetes' > lab/hello-cron.yaml
```

Edit `lab/hello-cron.yaml` to add `startingDeadlineSeconds: 17`:

```yaml
# lab/hello-cron.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello-cron
spec:
  schedule: "*/1 * * * *"
  startingDeadlineSeconds: 17
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello-cron
            image: busybox
            command:
            - /bin/sh
            - -c
            - date; echo Hello from Kubernetes
          restartPolicy: OnFailure
```

```bash
kubectl apply -f lab/hello-cron.yaml
kubectl get cj
# NAME         SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
# hello-cron   */1 * * * *   False     0        <none>          5s
```

## Checklist (Score: 0/6)

- [ ] Job `busybox-job` exists
- [ ] `busybox-job` has `completions: 5`
- [ ] `busybox-job` has `parallelism: 2`
- [ ] CronJob `hello-cron` exists with schedule `*/1 * * * *`
- [ ] `hello-cron` has `startingDeadlineSeconds: 17`
- [ ] `hello-cron` job pods print the date and greeting to stdout
