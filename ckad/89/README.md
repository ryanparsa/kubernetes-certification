# Question 89

> **Solve this question on:** `ckad-lab-89`

Team Neptune needs a *Job* for a one-time task. Create a *Job* named `neb-new-job` in *Namespace* `neptune`. The *Job* should run the command `sleep 2 && echo done` using image `busybox:1.31.0`. The *Job* should also be configured with:

- `completions: 3`
- `parallelism: 2`
- `activeDeadlineSeconds: 30`

The container should be named `neb-new-job-container`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
