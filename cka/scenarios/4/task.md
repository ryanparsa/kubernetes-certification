# Task 4 — Cluster Architecture: RBAC

**Context:** Cluster `cka-task-4` (`export KUBECONFIG=$PWD/kubeconfig`)

## Objective

In namespace `dev`, create:

1. A `ServiceAccount` named **`dev-reader`**.
2. A `Role` named **`pod-reader`** that grants **only** the verbs `get`, `list`, and `watch`
   on the `pods` resource (core API group).
3. A `RoleBinding` named **`dev-reader-binding`** that binds the `pod-reader` Role
   to the `dev-reader` ServiceAccount.

The ServiceAccount `dev-reader` must:
- Be able to `list pods` in namespace `dev`.
- **Not** be able to `list pods` in namespace `prod`.
- **Not** be able to `delete pods` in namespace `dev`.

## Verify

```
./test.sh
```
