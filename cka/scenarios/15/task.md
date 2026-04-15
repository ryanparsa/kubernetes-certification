# Task 15 — Workloads: ConfigMap & Secret Mounts

**Context:** Cluster `cka-task-15` (`export KUBECONFIG=$PWD/kubeconfig`)

In namespace `app`, the following already exist:

- ConfigMap `app-config` with keys `LOG_LEVEL`, `app.properties`
- Secret `app-secret` with keys `DB_PASSWORD`, `API_KEY`

## Objective

Create a Pod **`app-pod`** in namespace **`app`** that:

1. Runs a single container `web` from image `nginx:1.27-alpine`.
2. Mounts ConfigMap `app-config` as a **volume** at **`/etc/config`** (read-only).
3. Mounts Secret `app-secret` as a **volume** at **`/etc/secret`** with `defaultMode: 0400`.
4. Sets env var `LOG_LEVEL` from the `LOG_LEVEL` key of the `app-config` ConfigMap (via `valueFrom.configMapKeyRef`).
5. Sets env var `DB_PASSWORD` from the `DB_PASSWORD` key of the `app-secret` Secret (via `valueFrom.secretKeyRef`).

The Pod must be `Running`.

## Verify

```
./test.sh
```
