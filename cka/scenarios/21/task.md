# Task 21 — Workloads: Sidecar Logging

**Context:** Cluster `cka-task-21` (`export KUBECONFIG=$PWD/kubeconfig`)

A Pod named `app` is running a legacy application that writes logs to a file
at `/var/log/app.log` inside its container. Currently, `kubectl logs app -c main`
is empty because nothing is written to stdout.

## Objective

Update the Pod `app` in the `default` namespace to include a **sidecar container**:

1. Container name: **`sidecar`**
2. Image: **`busybox:1.36`**
3. Command: **`["/bin/sh", "-c", "tail -n+1 -f /var/log/app.log"]`**
4. The sidecar must share the same volume (`logs`) as the `main` container, mounted at `/var/log`.

The final Pod must have **two** containers, and `kubectl logs app -c sidecar`
must show the contents of the log file.

## Constraints

- Do **not** modify the `main` container's image or command.
- Since Pods are largely immutable, you will need to:
  - Export the current Pod to YAML.
  - Delete the Pod.
  - Modify the YAML to add the sidecar.
  - Re-create the Pod.

## Verify

```
./test.sh
```
