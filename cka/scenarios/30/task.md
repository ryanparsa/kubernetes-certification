# Task 30 — Troubleshooting: Service Selector Mismatch

**Context:** Cluster `cluster1` (`kubectl config use-context kubernetes-admin@cluster1`)

The `frontend` pod in namespace `prod` cannot reach the `backend` service.
Both pods are `Running 1/1`. The `backend` Service exists on port `8080`.

## Objective

1. Diagnose why the `backend` Service has no endpoints.
2. Fix the Service so traffic is routed to the `backend` pod.

## Constraints

- Do **not** delete and recreate the Service.
- Fix in place using `kubectl patch` or `kubectl edit`.
- Keep all other Service fields unchanged.

## Verify

```bash
kubectl -n prod get endpoints backend
# Expected: an IP:8080 entry — not <none>

kubectl -n prod exec deploy/frontend -- curl -s http://backend:8080
# Expected: a response from the backend pod
```
