# Question 26

> **Solve this question on:** `ckad-lab-26`

The system administration team needs an automated solution for log file cleanup.

Create a CronJob named `log-cleaner` in namespace `workloads` that will automatically manage log files based on age.

Configure it to run precisely every hour (using a standard cron expression) and use the `busybox` image. The job should execute the command `find /var/log -type f -name "*.log" -mtime +7 -delete` to remove log files older than 7 days.

To prevent resource contention, set the concurrency policy to `Forbid` so that new job executions are skipped if a previous execution is still running.

For job history management, configure the job to keep exactly `3` successful job completions and `1` failed job in its history.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
