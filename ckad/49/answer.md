## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/job/

### Create the namespace

```bash
kubectl create namespace jobs
```

### Create the Job

```yaml
# lab/49.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: jobs
---
apiVersion: batch/v1
kind: Job
metadata:
  name: data-processor
  namespace: jobs
spec:
  backoffLimit: 4
  activeDeadlineSeconds: 30
  template:
    spec:
      containers:
      - name: processor
        image: busybox
        command: ['sh', '-c', 'for i in $(seq 1 5); do echo Processing item $i; sleep 2; done']
      restartPolicy: Never
```

```bash
kubectl apply -f lab/49.yaml
```

### Verify

```bash
kubectl get job data-processor -n jobs
kubectl describe job data-processor -n jobs | grep -E "Backoff|Deadline|Restart"
kubectl logs -l job-name=data-processor -n jobs
```

## Checklist (Score: 0/4)

- [ ] Namespace `jobs` exists
- [ ] Job `data-processor` is created with image `busybox` and correct command
- [ ] Job has restart policy `Never` and backoff limit `4`
- [ ] Job has active deadline of `30` seconds
