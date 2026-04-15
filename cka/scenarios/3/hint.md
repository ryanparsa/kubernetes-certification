# Hints — Task 3

## Hint 1
The `etcdctl` binary is **not** installed on the kind node by default. You have two options:
1. Use `kubectl -n kube-system exec etcd-cka-task-3-control-plane -- etcdctl ...`
   (the etcd container ships with `etcdctl`).
2. Install `etcdctl` on the host node (`apt-get install -y etcd-client`).

The kubectl-exec approach is faster and more exam-realistic.

## Hint 2
Find the right cert paths from the etcd manifest:
```
docker exec cka-task-3-control-plane cat /etc/kubernetes/manifests/etcd.yaml | grep -E 'cert|key|endpoint'
```
You should see paths like `/etc/kubernetes/pki/etcd/{ca.crt,server.crt,server.key}`.

## Solution

```bash
kubectl -n kube-system exec etcd-cka-task-3-control-plane -- sh -c '
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
'
# Verify
kubectl -n kube-system exec etcd-cka-task-3-control-plane -- sh -c '
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db -w table \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
'
```

The file lives at `/tmp/etcd-backup.db` *inside the etcd pod's filesystem*. The grader
verifies it from the same location via `kubectl exec`.
