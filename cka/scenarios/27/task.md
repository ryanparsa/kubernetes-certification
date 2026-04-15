# Task 27 — Troubleshooting: ResourceQuota

**Context:** Cluster `cka-task-27` (`export KUBECONFIG=$PWD/kubeconfig`)

The `Deployment` named `limited-app` in the `quota-test` namespace is configured for
5 replicas, but only 2 pods are ever created.

## Objective

1. Diagnose why the `Deployment` is unable to scale to its desired replica count.
2. Fix the issue by **increasing the hard limit for pods** in the existing
   `ResourceQuota` named **`pod-quota`** to at least **10**.
3. Ensure the `limited-app` Deployment successfully scales to all **5 ready replicas**.

## Constraints

- Do **not** delete the `ResourceQuota` — modify the existing one.
- Do **not** modify the `Deployment`'s replica count.

## Verify

```
./test.sh
```
