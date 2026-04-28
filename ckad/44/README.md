# Question 44

> **Solve this question on:** `ckad-lab-44`

Create a CronJob in the `pod-design` namespace with the following specifications:

1. Name: `backup-job`
2. Schedule: Every 5 minutes
3. Container image: `busybox`
4. Command: `['sh', '-c', 'echo Backup started: $(date); sleep 30; echo Backup completed: $(date)']`
5. Configure the job with a restart policy of `OnFailure`
6. Set a deadline of `100` seconds for the job to complete

Ensure the namespace exists before creating the resource.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
