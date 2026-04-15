# Task 6 — Networking: Service Endpoints

**Context:** Cluster `cka-task-6` (`export KUBECONFIG=$PWD/kubeconfig`)

In namespace `shop` there is a `Deployment` named `web` (running, 2 replicas) and a
`Service` named `broken-svc`. However, traffic to the Service does not reach any pods.

## Objective

Diagnose and fix the issue so that:

- `kubectl -n shop get endpoints broken-svc` shows **two pod IPs** in the `ENDPOINTS` column.
- A test pod can `curl broken-svc.shop.svc.cluster.local` and get an HTTP 200 response.

## Constraints

- Do **not** rename or delete `broken-svc`.
- Do **not** change the Deployment's pod labels.

## Verify

```
./test.sh
```
