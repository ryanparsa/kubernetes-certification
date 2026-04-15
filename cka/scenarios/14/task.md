# Task 14 — Networking: Gateway API HTTPRoute

**Context:** Cluster `cka-task-14` (`export KUBECONFIG=$PWD/kubeconfig`)

The Gateway API standard CRDs are installed and a `GatewayClass` named `example-class` exists.
Namespace `shop` already contains two Services: `stable` and `canary` (both nginx on port 80).

## Objective

Create the following Gateway API resources in namespace `shop`:

1. A **`Gateway`** named **`shop-gw`** that uses the `example-class` GatewayClass and listens
   on **port 80** with protocol **HTTP**, hostname `shop.example.com`.
2. An **`HTTPRoute`** named **`shop-route`** attached to `shop-gw` that routes traffic for
   path prefix **`/`** to the two backends with a **canary split**:
   - `stable` Service on port 80 with **weight 90**
   - `canary` Service on port 80 with **weight 10**

The grader checks the structure of the resources only — no real controller is installed.

## Verify

```
./test.sh
```
