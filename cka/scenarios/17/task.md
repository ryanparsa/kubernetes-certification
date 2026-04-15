# Task 17 — Scheduling: Targeted DaemonSet

**Context:** Cluster `cka-task-17` (`export KUBECONFIG=$PWD/kubeconfig`)

The cluster has 1 control-plane and 2 workers (`cka-task-17-worker`, `cka-task-17-worker2`).
Only `cka-task-17-worker2` is labeled `monitoring=true`.

## Objective

In namespace `observability`, create a `DaemonSet` named **`node-exporter`** that:

- Uses image `nginx:1.27-alpine` (acts as a stand-in for the real exporter).
- Runs **only** on nodes with the label `monitoring=true`.
- Must end up with **exactly 1 pod**, scheduled on `cka-task-17-worker2`.

## Verify

```
./test.sh
```
