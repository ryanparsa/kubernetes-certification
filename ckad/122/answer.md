## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/controllers/job/>

```yaml
# lab/neb-new-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: neb-new-job
  namespace: neptune
spec:
  completions: 3
  parallelism: 2
  activeDeadlineSeconds: 30
  template:
    metadata:
      name: neb-new-job-pod
    spec:
      containers:
      - name: neb-new-job-container
        image: busybox:1.31.0
        command: ["sh", "-c", "sleep 2 && echo done"]
      restartPolicy: Never
```

```bash
kubectl apply -f lab/neb-new-job.yaml
kubectl get jobs -n neptune
kubectl get pods -n neptune
```

## Checklist (Score: 0/4)

- [ ] Job `neb-new-job` exists in Namespace `neptune`
- [ ] Job configured with `completions: 3`, `parallelism: 2`, `activeDeadlineSeconds: 30`
- [ ] Pod named `neb-new-job-pod`, container named `neb-new-job-container`
- [ ] Container uses image `busybox:1.31.0` and runs `sleep 2 && echo done`
