## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/job/

### Create the namespace (if not present)

```bash
kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
```

### Create the Job

```yaml
# lab/hello-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello-job
  namespace: networking
spec:
  activeDeadlineSeconds: 30
  backoffLimit: 0
  template:
    spec:
      containers:
      - name: hello
        image: busybox
        command: ["sh", "-c", "echo 'Hello from Kubernetes job!'"]
      restartPolicy: Never
```

```bash
kubectl apply -f lab/hello-job.yaml
```

### Verify

```bash
kubectl get job hello-job -n networking
kubectl get pods -n networking -l job-name=hello-job
kubectl logs -n networking -l job-name=hello-job
```

## Checklist (Score: 0/3)

- [ ] Job `hello-job` exists in namespace `networking`
- [ ] Job uses image `busybox`, has `activeDeadlineSeconds: 30`, and `restartPolicy: Never`
- [ ] Job completes successfully and logs show `Hello from Kubernetes job!`
