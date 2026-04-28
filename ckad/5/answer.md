## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/job/

### Job 1 — pi

```yaml
# lab/pi.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: pi
        image: perl:5.34
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
```

```bash
kubectl apply -f lab/pi.yaml
kubectl wait job/pi --for=condition=Complete --timeout=120s
kubectl logs job/pi
```

The output is pi to 2000 decimal places.

### Job 2 — multi (5 completions, parallelism 2)

```yaml
# lab/multi.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: multi
spec:
  completions: 5
  parallelism: 2
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: multi
        image: busybox
        command: ["echo", "done"]
```

```bash
kubectl apply -f lab/multi.yaml
kubectl wait job/multi --for=condition=Complete --timeout=60s
kubectl get job multi
```

The `COMPLETIONS` column should show `5/5`.

### Job 3 — deadline (activeDeadlineSeconds)

```yaml
# lab/deadline.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: deadline
spec:
  activeDeadlineSeconds: 30
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: deadline
        image: busybox
        command: ["sleep", "60"]
```

```bash
kubectl apply -f lab/deadline.yaml
# Wait ~30 seconds, then observe
kubectl get job deadline
kubectl describe job deadline | grep -A5 "Conditions:"
```

The job will be terminated with reason `DeadlineExceeded`.

## Checklist (Score: 0/4)

- [ ] Job `pi` completed successfully
- [ ] `kubectl logs job/pi` shows pi digits
- [ ] Job `multi` reaches 5/5 completions with `parallelism: 2`
- [ ] Job `deadline` is terminated by `activeDeadlineSeconds: 30`
