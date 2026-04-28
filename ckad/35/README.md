# Question 35

> **Solve this question on:** `ckad-lab-35`

Create a simple batch processing task to demonstrate the Job resource type.

Create a Kubernetes Job named `hello-job` in the `networking` namespace that runs a pod with the `busybox` image.

The job should execute a single command that prints `Hello from Kubernetes job!` to standard output, and then completes successfully.

Configure the job to:

1. Run only once and not be restarted after completion
2. Have a deadline of `30` seconds (the job will be terminated if it doesn't complete within this time)
3. Use `Never` as the restart policy for the pod

This job demonstrates the basic pattern for one-time task execution in Kubernetes.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
