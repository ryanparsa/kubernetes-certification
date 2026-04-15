# Task 29 — Troubleshooting: Liveness Probe Port Mismatch

**Context:** Cluster `cluster1` (`kubectl config use-context kubernetes-admin@cluster1`)

The `api-server` Deployment in namespace `web` is not serving traffic.
Its pod has been running for 9 minutes with 6 restarts and is never `Ready`.

## Objective

1. Diagnose why the pod keeps restarting using `kubectl describe`.
2. Fix the Deployment so the pod reaches `Running` and `Ready (1/1)`.

## Constraints

- Do **not** delete and recreate the Deployment.
- Fix in place using `kubectl patch` or `kubectl edit`.
- Keep the image (`nginx:1.25`), replica count, and all other fields unchanged.

## Verify

```bash
kubectl -n web rollout status deployment/api-server
kubectl -n web get pods
# Expected: 1/1 Running, 0 recent restarts
```
