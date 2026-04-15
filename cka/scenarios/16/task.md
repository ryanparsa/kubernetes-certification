# Task 16 — Workloads: Rolling Update Rollback

**Context:** Cluster `cka-task-16` (`export KUBECONFIG=$PWD/kubeconfig`)

The Deployment `shop/store` was updated to a broken image. New pods are stuck in
`ImagePullBackOff`. The previous revision was healthy.

## Objective

Roll back `shop/store` to the **previous working revision** so that:

- The Deployment has **3 ready replicas**.
- The container image is back to `nginx:1.27-alpine`.

Use `kubectl rollout` commands — do **not** edit the Deployment manifest manually.

## Verify

```
./test.sh
```
