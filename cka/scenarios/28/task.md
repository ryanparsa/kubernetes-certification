# Task 28 — Scheduling: Static Pods on Worker Nodes

**Context:** Cluster `cka-task-28` (`export KUBECONFIG=$PWD/kubeconfig`)

The security team requires a monitoring agent to run on the worker node
`cka-task-28-worker` independent of the API server's control.

## Objective

Create a **Static Pod** on worker node **`cka-task-28-worker`**:

1. Pod Name: **`agent`**
2. Image: **`nginx:1.27-alpine`**
3. Manifest location: **`/etc/kubernetes/manifests/`** on the worker node.
4. Container resources: **`requests.cpu: 10m`**, **`requests.memory: 20Mi`**.

## Steps

1. SSH into the worker: `docker exec -it cka-task-28-worker bash`.
2. Find the Kubelet's `staticPodPath` in `/var/lib/kubelet/config.yaml`.
3. Create the manifest file in that directory.

The Pod should eventually appear in `kubectl get pods -A` with a name
like `agent-cka-task-28-worker`.

## Verify

```
./test.sh
```
