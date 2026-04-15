# Task 20 — Troubleshooting: Kubelet Service

**Context:** Cluster `cka-task-20` (`export KUBECONFIG=$PWD/kubeconfig`)

Worker node `cka-task-20-worker` is `NotReady`. It seems the `kubelet` service is failing
to start or configuration is invalid.

## Objective

1. SSH into the worker: `docker exec -it cka-task-20-worker bash`.
2. Find why the `kubelet` is failing using standard system tools (`systemctl`, `journalctl`).
3. Correct the error in the `kubelet` configuration file (located in `/var/lib/kubelet/config.yaml`).
4. Restart the `kubelet` service.
5. The worker node must return to `Ready` status.

## Verify

```
./test.sh
```
