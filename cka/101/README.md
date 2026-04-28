# Question 101

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Create a single *Pod* of image `httpd:2.4.41-alpine` in *Namespace* `default`. The *Pod* should be named `pod` and the container should be named `pod-container`. This *Pod* should only be scheduled on a master node — do not add any tolerations.
