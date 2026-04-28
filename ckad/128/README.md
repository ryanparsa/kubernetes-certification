# Question 128

> **Solve this question on:** `ckad-lab-128`

In *Namespace* `pluto` there is a *Deployment* named `pluto-deployment`. The *Pods* managed by this *Deployment* should have a `sidecar` container named `sidecar` added to them.

The sidecar container should use image `busybox:1.31.0` and run the command `sh -c 'while true; do date >> /var/log/date.log; sleep 1; done'`.

The `sidecar` container should mount the existing volume named `log-data` at `/var/log`. The `pluto-app` container should mount it at `/tmp/log`.

You could use the existing `docker.io` registry or any accessible registry.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
