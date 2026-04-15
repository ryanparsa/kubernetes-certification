# Task 2 — Troubleshooting: Broken Control Plane

**Context:** Cluster `cka-task-2` (`export KUBECONFIG=$PWD/kubeconfig`)

The cluster's control plane has been sabotaged. Running `kubectl get nodes` will time out
or return connection errors within ~30 seconds of cluster startup.

The control-plane node is a docker container named `cka-task-2-control-plane`.
You can "SSH" into it with:

```
docker exec -it cka-task-2-control-plane bash
```

Static pod manifests live in `/etc/kubernetes/manifests/` on that node.

## Objective

Restore the cluster to a healthy state so that:

- `kubectl get nodes` returns the control-plane node as `Ready`.
- All `kube-system` core pods (`kube-apiserver`, `kube-controller-manager`, `kube-scheduler`, `etcd`) are `Running`.

## Hints (allowed kubectl commands once API recovers)

- `kubectl -n kube-system get pods`
- `crictl ps -a` from inside the node when API is down

## Verify

```
./test.sh
```
