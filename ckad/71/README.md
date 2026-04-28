# Question 71

> **Solve this question on:** `ckad-lab-71`

1. Create a *Job* named `busybox-job` with the `busybox` image that runs the command `/bin/sh -c 'echo hello; sleep 5; echo world'` with **5 completions** and **2 parallel** pods.

2. Create a *CronJob* named `hello-cron` with the `busybox` image that runs the command `/bin/sh -c 'date; echo Hello from Kubernetes'` on a schedule of `*/1 * * * *`. Set `startingDeadlineSeconds: 17`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
