# Task 9 — Troubleshooting: NotReady Worker Node

**Context:** Cluster `cka-task-9` (`export KUBECONFIG=$PWD/kubeconfig`)

`kubectl get nodes` reports the worker node `cka-task-9-worker` as `NotReady`.
A `Deployment` named `hello` (4 replicas) cannot fully schedule.

The control-plane node is fine. Investigate the worker — `docker exec` into it to mimic
SSHing into a real worker:

```
docker exec -it cka-task-9-worker bash
```

## Objective

Restore the worker to `Ready` so that all 4 `hello` replicas become `Ready`.

## Verify

```
./test.sh
```
