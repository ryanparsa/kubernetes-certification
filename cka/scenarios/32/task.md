# Task 32 — Troubleshooting: Missing CA Certificate (Controller Manager Down)

**Context:** Cluster `cluster1` (`kubectl config use-context kubernetes-admin@cluster1`)

`kube-controller-manager` is in `CrashLoopBackOff`. All other control plane components are healthy.

```
$ kubectl get pods -n kube-system
NAME                                    READY   STATUS             RESTARTS   AGE
etcd-controlplane                       1/1     Running            0          5d
kube-apiserver-controlplane             1/1     Running            0          5d
kube-controller-manager-controlplane    0/1     CrashLoopBackOff   8          18m
kube-scheduler-controlplane             1/1     Running            0          5d
```

## Objective

1. Diagnose why `kube-controller-manager` is crash-looping.
2. Fix it so the pod reaches `Running 1/1` without restarting.

## Constraints

- Do not delete or recreate the static pod manifest.
- Do not run `kubeadm init` (full reinit).

## Verify

```bash
kubectl -n kube-system get pod kube-controller-manager-controlplane
# Expected: 1/1 Running, low restart count
```
