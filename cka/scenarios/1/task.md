# Task 1 — Troubleshooting: CrashLoopBackOff

**Context:** Cluster `cka-task-1` (`export KUBECONFIG=$PWD/assets/kubeconfig`)

A `Deployment` named `crashy` in namespace `troubleshoot` is failing.
Its pods enter `CrashLoopBackOff` shortly after starting.

## Objective

1. Diagnose why the pods are crashing using only `kubectl` (logs, describe, etc.).
2. Fix the `Deployment` so that **all 3 replicas reach `Running` and stay `Ready`**.

## Constraints

- Do **not** delete the `Deployment` and recreate from scratch — patch or edit it in place.
- Keep the namespace, name, replica count, image (`busybox:1.36`), and labels unchanged.
- The container must remain a long-running process (not exit immediately).

## Verify

```
./test.sh
```
