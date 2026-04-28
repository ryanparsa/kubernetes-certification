# Question 41

> **Solve this question on:** `cka-lab-41`

Create a pod named `logger` in the `monitoring` namespace with two containers:

1. A `busybox` container that writes logs to `/var/log/app.log`
2. A `fluentd` container that reads logs from the same location

Use an `emptyDir` volume named `log-volume` to share logs between containers. Mount this volume at `/var/log` in both containers.

Ensure both containers are running.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
