# Task 24 — Networking: Ingress Resource

**Context:** Cluster `cka-task-24` (`export KUBECONFIG=$PWD/kubeconfig`)

Namespace `internal` contains a Service named `api-service` listening on port 80.

## Objective

Create an **Ingress** resource named **`api-ingress`** in the **`internal`** namespace with:

- Host: **`api.example.com`**
- Path: **`/v1`**
- Path Type: **`Prefix`**
- Backend Service: **`api-service`** on port **80**.

The grader checks the resource structure.

## Verify

```
./test.sh
```
