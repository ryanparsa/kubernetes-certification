# Task 7 — Workloads & Scheduling

**Context:** Cluster `cka-task-7` (`export KUBECONFIG=$PWD/kubeconfig`)

The cluster has one worker node `cka-task-7-worker` that has been:
- Tainted with `tier=critical:NoSchedule`
- Labeled with `disk=ssd`

The control-plane node has neither.

## Objective

Create a `Deployment` named **`priority-app`** in the **default** namespace with:

- **3 replicas** of `nginx:1.27-alpine`.
- A **toleration** for the taint `tier=critical:NoSchedule`.
- A **`requiredDuringSchedulingIgnoredDuringExecution` nodeAffinity** requiring label `disk=ssd`.
- Container resources: `requests.cpu: 100m`, `limits.cpu: 200m`.

All 3 pods must end up `Running` on the worker node `cka-task-7-worker`.

## Verify

```
./test.sh
```
