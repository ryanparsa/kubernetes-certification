# Task 11 — Cluster Architecture: Helm

**Context:** Cluster `cka-task-11` (`export KUBECONFIG=$PWD/kubeconfig`)

A local Helm chart is available at `./charts/web` in this directory. It defines a simple
nginx Deployment and Service. Default values: `replicaCount=1`, `serviceType=ClusterIP`.

## Objective

Use **Helm** (not raw `kubectl apply`) to:

1. Install the chart `./charts/web` as release **`frontend`** in namespace **`platform`**.
2. Override values so that the resulting Deployment has **3 replicas** and the Service is of
   type **`NodePort`**.

The release must show as `deployed` in `helm list -n platform`.

## Verify

```
./test.sh
```
