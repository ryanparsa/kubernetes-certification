# Task 10 — Networking: Cluster DNS Failure

**Context:** Cluster `cka-task-10` (`export KUBECONFIG=$PWD/kubeconfig`)

In-cluster DNS resolution is broken. From any pod, `nslookup web.probe.svc.cluster.local`
times out or returns `SERVFAIL`. The Service `probe/web` exists and has healthy endpoints.

## Objective

Restore in-cluster DNS so that:
- `kubectl -n kube-system get pods -l k8s-app=kube-dns` shows at least 1 `Running` CoreDNS pod.
- A test pod in any namespace can resolve `web.probe.svc.cluster.local` to the Service ClusterIP.

Do **not** modify the existing `coredns` Deployment image or its ConfigMap.

## Verify

```
./test.sh
```
