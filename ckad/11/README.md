# Question 11

> **Solve this question on:** `ckad-lab-11`

Perform the following observability tasks:

1. Create a pod named `probe-pod` with image `nginx` exposing container port `80`. Configure:
   - A **liveness probe** using HTTP GET on path `/` port `80`, with `initialDelaySeconds: 10` and `periodSeconds: 5`
   - A **readiness probe** using HTTP GET on path `/` port `80`, with `initialDelaySeconds: 5` and `periodSeconds: 5`

2. Create a pod named `broken` with image `busybox` and command `ls /notexist`. The pod will fail. Use `kubectl logs` and `kubectl describe` to identify the error message. Document what you observe.
