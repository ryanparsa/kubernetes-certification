# Task 18 — Workloads: HorizontalPodAutoscaler

**Context:** Cluster `cka-task-18` (`export KUBECONFIG=$PWD/kubeconfig`)

The Deployment `web/shop` exists with 1 replica but **does not** declare CPU requests
(an HPA can't compute target utilization without them).

## Objective

1. Patch the `web/shop` Deployment so its container has `resources.requests.cpu: 200m`
   and `resources.limits.cpu: 500m`.
2. Create a `HorizontalPodAutoscaler` named **`shop-hpa`** in namespace `web`, targeting
   the `shop` Deployment, with:
   - `minReplicas: 2`
   - `maxReplicas: 6`
   - Average **CPU utilization target: 60%**
   - Use the `autoscaling/v2` API.

The Deployment must end up with at least **2** ready replicas (HPA will scale it from 1).

## Verify

```
./test.sh
```
