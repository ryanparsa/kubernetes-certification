# Question 87

> **Solve this question on:** `ckad-lab-87`

Create a namespace `jobs`.

Create a CronJob named `backup-job` in namespace `jobs` with the following specification:

- **Schedule**: every day at 02:00 AM (`0 2 * * *`)
- **Image**: `busybox`
- **Command**: `sh -c 'echo "Backup started at $(date)" && sleep 5 && echo "Backup complete"'`
- `successfulJobsHistoryLimit: 3`
- `failedJobsHistoryLimit: 1`
- `concurrencyPolicy: Forbid`

Verify the CronJob is created:

```bash
kubectl get cronjob backup-job -n jobs
```

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
