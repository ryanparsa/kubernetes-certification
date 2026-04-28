# Question 128

> **Solve this question on:** `ckad-lab-09`

In *Namespace* `pluto` there is a single *Pod* named `pluto-pod`. This *Pod* has been deployed by a *Deployment* named `pluto-deployment`. The *Pod* should have the `sidecar` container named `sidecar` added to it.

The sidecar container should use image `busybox:1.31.0` and run the command `sh -c 'while true; do date >> /var/log/date.log; sleep 1; done'`.

The `sidecar` container should mount the existing volume named `log-data` at `/var/log`. The `pluto-app` container should mount it at `/tmp/log`.

You could use the existing `docker.io` registry or any accessible registry.
