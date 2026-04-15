# Task 31 — Troubleshooting: Kubelet Won't Start (Bad Config Path)

**Context:** Cluster `cluster1` (`kubectl config use-context kubernetes-admin@cluster1`)

`worker-2` is in `NotReady` state. Pods are not being scheduled onto it.

```
$ kubectl get nodes
NAME           STATUS     ROLES           AGE   VERSION
controlplane   Ready      control-plane   4d    v1.34.0
worker-1       Ready      <none>          4d    v1.34.0
worker-2       NotReady   <none>          4d    v1.34.0
```

## Objective

1. SSH into `worker-2` and diagnose why the kubelet is not running.
2. Fix the kubelet so that `worker-2` returns to `Ready`.

## Constraints

- Do not replace or recreate any certificates or kubeconfig files.
- Fix must survive a kubelet restart.

## Verify

```bash
# on worker-2
systemctl status kubelet
# Expected: Active: running

# on controlplane
kubectl get nodes worker-2
# Expected: Ready
```
