# Question 132

> **Solve this question on:** `ckad-lab-13`

Create a *Pod* named `pod-13` in *Namespace* `default` using image `busybox:1.31.0`. Configure a `livenessProbe` which simply runs `true`. Also configure a `readinessProbe` which does check if the URL `http://service-13:80` is reachable, you can use `wget -T2 -O- http://service-13` for this.

The `initialDelaySeconds` of the `readinessProbe` should be 15, `periodSeconds` should be 5.

The *Pod* should also be configured to allow rescheduling to different nodes.
