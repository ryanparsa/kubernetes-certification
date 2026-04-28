# Question 131

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Create a single *Pod* of image `httpd:2.4.41-alpine` in *Namespace* `account`. The *Pod* should be named `pod` and the container should be named `pod-container`. This *Pod* should **only** be scheduled on controlplane nodes — do not add any tolerations.
