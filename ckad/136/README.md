# Question 136

> **Solve this question on:** `ckad-lab-17`

You are asked to find out about the container image used by the *Deployment* `war-department` and to also log out which entry points are used. You can find this in a log output somewhere.

Create a new *Pod* named `war-department-check` in *Namespace* `default` using image `busybox:1.31.0`. Configure the *Pod* to run `sleep 9999` and keep running. Mount the configuration from the existing *ConfigMap* `war-department-config` in Namespace `war` as a volume at path `/tmp/war-config`.

Write the log output of the running *Pod* into `/opt/course/17/pod_logs.log`.
