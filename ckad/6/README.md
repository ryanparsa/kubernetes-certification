# Question 6

> **Solve this question on:** `ckad-lab-6`

Perform the following CronJob tasks:

1. Create a CronJob named `logger` with image `busybox` that runs on schedule `*/1 * * * *` (every minute) and executes the command `date; echo Hello from the cluster`.

2. Manually trigger a Job from the `logger` CronJob using `kubectl create job` without waiting for the next scheduled run.

3. Create a CronJob named `limited` with image `busybox` that runs on schedule `*/1 * * * *` and executes `date`, but sets `startingDeadlineSeconds: 17` so it will not start if it is more than 17 seconds late.
