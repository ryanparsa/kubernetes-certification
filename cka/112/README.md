# Question 112

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Create a *Pod* named `multi-container-playground` in *Namespace* `default` with **3 containers** named `c1`, `c2`, and `c3`:

- **c1**: image `nginx:1.17.6-alpine`. Have the name of the node where its *Pod* is running available as environment variable `MY_NODE_NAME` (use `fieldRef: fieldPath: spec.nodeName`)

- **c2**: image `busybox:1.31.1`. Write the output of `date` every second to the shared volume at `/var/log/date.log`:
  ```sh
  while true; do date >> /var/log/date.log; sleep 1; done
  ```

- **c3**: image `busybox:1.31.1`. Continuously read from the shared volume and write to stdout:
  ```sh
  tail -f /var/log/date.log
  ```

Check the logs of container `c3` to confirm the setup.
