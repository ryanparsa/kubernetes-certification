# Task 5 — Networking: NetworkPolicy

**Context:** Cluster `cka-task-5` (`export KUBECONFIG=$PWD/kubeconfig`)

Namespace `web` contains three pods: `api` (label `app=api`), `frontend` (label `role=frontend`),
and `other` (label `role=other`).

## Objective

Create the following two `NetworkPolicy` resources in namespace `web`:

1. **`default-deny`** — denies **all ingress** traffic to **all pods** in the `web` namespace.
2. **`allow-frontend-to-api`** — allows ingress traffic to pods labeled `app=api`,
   **only from pods labeled `role=frontend`** in the same namespace,
   and **only on TCP port 8080**.

The grader checks the structure of the policies, not live enforcement.

## Verify

```
./test.sh
```
