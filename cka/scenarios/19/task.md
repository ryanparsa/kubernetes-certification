# Task 19 — Cluster Maintenance: Node Drain

**Context:** Cluster `cka-task-19` (`export KUBECONFIG=$PWD/kubeconfig`)

Worker node `cka-task-19-worker` needs maintenance. It currently hosts a `Deployment`
named `legacy-app` that uses a static `nodeName` assignment (which prevents normal eviction).

## Objective

1. **Cordon** the worker node `cka-task-19-worker` so no new pods are scheduled.
2. **Drain** the node `cka-task-19-worker`. You must bypass the `nodeName` constraint and ignore any local data.
3. Ensure that after the drain, the node is in `SchedulingDisabled` status and has **no pods** from the `legacy-app` Deployment running on it.

## Verify

```
./test.sh
```
