# Question 135

> **Solve this question on:** `ckad-lab-16`

A team needs to be alerted when their three data-logging containers fail. To achieve this you need to configure a liveness probe for some logging data streams.

1. Find the existing *Deployment* named `cleaner` (or similar) and use the image `logger-col`. Also make sure that the *Deployment* is running in background.

2. Find the *Deployment* named `cleaner` using `kubectl get deployment cleaner -n pluto`, but also make sure the *Deployment* is running.

3. Create a sidecar container named `logger-col` using image `busybox:1.31.0` which runs in the background and keeps running. This sidecar should mount the same volume and write logs to a file `/var/log/cleaner/cleaner.log`.

4. Check the top of the two container output. The use case would be to print the lines from `/var/log/cleaner/cleaner.log` using `kubectl logs` by `--container logger-col`.
